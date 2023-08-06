"""Construct and collect pytd definitions to build a TypeDeclUnit."""

import collections

from typing import Any, Dict, List, Optional, Union

import dataclasses

from pytype.pyi import classdef
from pytype.pyi import types
from pytype.pyi.types import ParseError  # pylint: disable=g-importing-member
from pytype.pytd import escape
from pytype.pytd import pytd
from pytype.pytd import pytd_utils
from pytype.pytd import visitors
from pytype.pytd.codegen import function
from pytype.pytd.codegen import namedtuple
from pytype.pytd.codegen import pytdgen
from pytype.pytd.parse import node as pytd_node

from typed_ast import ast3


# Typing members that represent sets of types.
_TYPING_SETS = ("typing.Intersection", "typing.Optional", "typing.Union")


def _split_definitions(defs: List[Any]):
  """Return [constants], [functions] given a mixed list of definitions."""
  constants = []
  functions = []
  aliases = []
  slots = None
  classes = []
  for d in defs:
    if isinstance(d, pytd.Class):
      classes.append(d)
    elif isinstance(d, pytd.Constant):
      if d.name == "__slots__":
        pass  # ignore definitions of __slots__ as a type
      else:
        constants.append(d)
    elif isinstance(d, function.NameAndSig):
      functions.append(d)
    elif isinstance(d, pytd.Alias):
      aliases.append(d)
    elif isinstance(d, types.SlotDecl):
      if slots is not None:
        raise ParseError("Duplicate __slots__ declaration")
      slots = d.slots
    elif isinstance(d, types.Ellipsis):
      pass
    elif isinstance(d, ast3.Expr):
      raise ParseError("Unexpected expression").at(d)
    else:
      msg = "Unexpected definition"
      lineno = None
      if isinstance(d, ast3.AST):
        lineno = getattr(d, "lineno", None)
      raise ParseError(msg, line=lineno)
  return constants, functions, aliases, slots, classes


def _maybe_resolve_alias(alias, name_to_class, name_to_constant):
  """Resolve the alias if possible.

  Args:
    alias: A pytd.Alias
    name_to_class: A class map used for resolution.
    name_to_constant: A constant map used for resolution.

  Returns:
    None, if the alias pointed to an un-aliasable type.
    The resolved value, if the alias was resolved.
    The alias, if it was not resolved.
  """
  if not isinstance(alias.type, pytd.NamedType):
    return alias
  if alias.type.name in _TYPING_SETS:
    # Filter out aliases to `typing` members that don't appear in typing.pytd
    # to avoid lookup errors.
    return None
  if "." not in alias.type.name:
    # We'll handle nested classes specially, since they need to be represented
    # as constants to distinguish them from imports.
    return alias
  parts = alias.type.name.split(".")
  if parts[0] not in name_to_class and parts[0] not in name_to_constant:
    return alias
  prev_value = None
  value = name_to_class.get(parts[0]) or name_to_constant[parts[0]]
  for part in parts[1:]:
    prev_value = value
    # We can immediately return upon encountering an error, as load_pytd will
    # complain when it can't resolve the alias.
    if isinstance(value, pytd.Constant):
      if (not isinstance(value.type, pytd.NamedType) or
          value.type.name not in name_to_class):
        # TODO(rechen): Parameterized constants of generic classes should
        # probably also be allowed.
        return alias
      value = name_to_class[value.type.name]
    if not isinstance(value, pytd.Class):
      return alias
    try:
      value = value.Lookup(part)
    except KeyError:
      return alias
  if isinstance(value, pytd.Class):
    return pytd.Constant(
        alias.name, pytdgen.pytd_type(pytd.NamedType(alias.type.name)))
  elif isinstance(value, pytd.Function):
    # We allow module-level aliases of methods from classes and class instances.
    # When a static method is aliased, or a normal method is aliased from a
    # class (not an instance), the entire method signature is copied. Otherwise,
    # the first parameter ('self' or 'cls') is dropped.
    new_value = value.Replace(name=alias.name).Replace(kind="method")
    if value.kind == "staticmethod" or (
        value.kind == "method" and isinstance(prev_value, pytd.Class)):
      return new_value
    return new_value.Replace(signatures=tuple(
        s.Replace(params=s.params[1:]) for s in new_value.signatures))
  else:
    return value.Replace(name=alias.name)


class _InsertTypeParameters(visitors.Visitor):
  """Visitor for inserting TypeParameter instances."""

  def __init__(self, type_params):
    super().__init__()
    self.type_params = {p.name: p for p in type_params}

  def VisitNamedType(self, node):
    if node.name in self.type_params:
      return self.type_params[node.name]
    else:
      return node


class _VerifyMutators(visitors.Visitor):
  """Visitor for verifying TypeParameters used in mutations are in scope."""

  def __init__(self):
    super().__init__()
    # A stack of type parameters introduced into the scope. The top of the stack
    # contains the currently accessible parameter set.
    self.type_params_in_scope = [set()]
    self.current_function = None

  def _AddParams(self, params):
    top = self.type_params_in_scope[-1]
    self.type_params_in_scope.append(top | params)

  def _GetTypeParameters(self, node):
    collector = visitors.CollectTypeParameters()
    node.Visit(collector)
    return {x.name for x in collector.params}

  def EnterClass(self, node):
    params = set()
    for cls in node.parents:
      params |= self._GetTypeParameters(cls)
    self._AddParams(params)

  def LeaveClass(self, _):
    self.type_params_in_scope.pop()

  def EnterFunction(self, node):
    self.current_function = node
    params = set()
    for sig in node.signatures:
      for arg in sig.params:
        params |= self._GetTypeParameters(arg.type)
    self._AddParams(params)

  def LeaveFunction(self, _):
    self.type_params_in_scope.pop()
    self.current_function = None

  def EnterParameter(self, node):
    if isinstance(node.mutated_type, pytd.GenericType):
      params = self._GetTypeParameters(node.mutated_type)
      extra = params - self.type_params_in_scope[-1]
      if extra:
        fn = pytd_utils.Print(self.current_function)
        msg = "Type parameter(s) {%s} not in scope in\n\n%s" % (
            ", ".join(sorted(extra)), fn)
        raise ParseError(msg)


class _ContainsAnyType(visitors.Visitor):
  """Check if a pytd object contains a type of any of the given names."""

  def __init__(self, type_names):
    super().__init__()
    self._type_names = set(type_names)
    self.found = False

  def EnterNamedType(self, node):
    if node.name in self._type_names:
      self.found = True


def _contains_any_type(ast, type_names):
  """Convenience wrapper for _ContainsAnyType."""
  out = _ContainsAnyType(type_names)
  ast.Visit(out)
  return out.found


class _PropertyToConstant(visitors.Visitor):
  """Convert some properties to constant types."""

  def EnterTypeDeclUnit(self, node):
    self.type_param_names = [x.name for x in node.type_params]
    self.const_properties = []

  def LeaveTypeDeclUnit(self, node):
    self.type_param_names = None

  def EnterClass(self, node):
    self.const_properties.append([])

  def LeaveClass(self, node):
    self.const_properties.pop()

  def VisitClass(self, node):
    constants = list(node.constants)
    for fn in self.const_properties[-1]:
      ptypes = [x.return_type for x in fn.signatures]
      constants.append(
          pytd.Constant(name=fn.name, type=pytd_utils.JoinTypes(ptypes)))
    methods = [x for x in node.methods if x not in self.const_properties[-1]]
    return node.Replace(constants=tuple(constants), methods=tuple(methods))

  def EnterFunction(self, node):
    if (self.const_properties and
        node.kind == pytd.PROPERTY and
        not self._is_parametrised(node)):
      self.const_properties[-1].append(node)

  def _is_parametrised(self, method):
    for sig in method.signatures:
      if _contains_any_type(sig.return_type, self.type_param_names):
        return True


class Definitions:
  """Collect definitions used to build a TypeDeclUnit."""

  ELLIPSIS = types.Ellipsis()  # Object to signal ELLIPSIS as a parameter.

  def __init__(self, module_info):
    self.module_info = module_info
    self.type_map: Dict[str, Any] = {}
    self.constants = []
    self.aliases = collections.OrderedDict()
    self.type_params = []
    self.generated_classes = collections.defaultdict(list)
    self.module_path_map = {}

  def add_alias_or_constant(self, alias_or_constant):
    """Add an alias or constant.

    Args:
      alias_or_constant: the top-level definition to add.

    Raises:
      ParseError: For an invalid __slots__ declaration.
    """
    if isinstance(alias_or_constant, pytd.Constant):
      self.constants.append(alias_or_constant)
    elif isinstance(alias_or_constant, types.SlotDecl):
      raise ParseError("__slots__ only allowed on the class level")
    elif isinstance(alias_or_constant, pytd.Alias):
      name, value = alias_or_constant.name, alias_or_constant.type
      self.type_map[name] = value
      self.aliases[name] = alias_or_constant
    else:
      assert False, "Unknown type of assignment"

  def new_new_type(self, name, typ):
    """Returns a type for a NewType."""
    args = [("self", pytd.AnythingType()), ("val", typ)]
    ret = pytd.NamedType("NoneType")
    methods = function.merge_method_signatures(
        [function.NameAndSig.make("__init__", args, ret)])
    cls_name = escape.pack_newtype_base_class(
        name, len(self.generated_classes[name]))
    cls = pytd.Class(name=cls_name,
                     metaclass=None,
                     parents=(typ,),
                     methods=tuple(methods),
                     constants=(),
                     decorators=(),
                     classes=(),
                     slots=None,
                     template=())
    self.generated_classes[name].append(cls)
    return pytd.NamedType(cls_name)

  def new_named_tuple(self, base_name, fields):
    """Return a type for a named tuple (implicitly generates a class).

    Args:
      base_name: The named tuple's name.
      fields: A list of (name, type) tuples.

    Returns:
      A NamedType() for the generated class that describes the named tuple.
    """
    nt = namedtuple.NamedTuple(base_name, fields, self.generated_classes)
    self.generated_classes[base_name].append(nt.cls)
    self.type_params.append(nt.type_param)
    return pytd.NamedType(nt.name)

  def new_typed_dict(self, name, items, total):
    """Returns a type for a TypedDict.

    This method is currently called only for TypedDict objects defined via
    the following function-based syntax:

      Foo = TypedDict('Foo', {'a': int, 'b': str}, total=False)

    rather than the recommended class-based syntax.

    Args:
      name: the name of the TypedDict instance, e.g., "'Foo'".
      items: a {key: value_type} dict, e.g., {"'a'": "int", "'b'": "str"}.
      total: A tuple of a single kwarg, e.g., ("total", NamedType("False")), or
        None when no kwarg is passed.
    """
    # TODO(b/157603915): Add real support for TypedDict.
    del name, items, total  # unused
    return pytd.GenericType(
        pytd.NamedType("typing.Dict"),
        (pytd.NamedType("str"), pytd.NamedType("typing.Any")))

  def add_type_var(self, name, typevar):
    """Add a type variable, <name> = TypeVar(<name_arg>, <args>)."""
    if name != typevar.name:
      raise ParseError("TypeVar name needs to be %r (not %r)" % (
          typevar.name, name))
    bound = typevar.bound
    if isinstance(bound, str):
      bound = pytd.NamedType(bound)
    constraints = tuple(typevar.constraints) if typevar.constraints else ()
    self.type_params.append(pytd.TypeParameter(
        name=name, constraints=constraints, bound=bound))

  def add_import(self, from_package, import_list):
    """Add an import.

    Args:
      from_package: A dotted package name if this is a "from" statement, or None
          if it is an "import" statement.
      import_list: A list of imported items, which are either strings or pairs
          of strings.  Pairs are used when items are renamed during import
          using "as".
    """
    if from_package:
      # from a.b.c import d, ...
      for item in import_list:
        t = self.module_info.process_from_import(from_package, item)
        self.type_map[t.new_name] = t.pytd_node
        if (isinstance(item, tuple) or
            from_package != "typing" or
            self.module_info.module_name == "protocols"):
          self.aliases[t.new_name] = t.pytd_alias()
          self.module_path_map[t.new_name] = t.qualified_name
    else:
      # import a, b as c, ...
      for item in import_list:
        t = self.module_info.process_import(item)
        if t:
          self.aliases[t.new_name] = t.pytd_alias()

  def _matches_full_name(self, t, full_name):
    """Whether t.name matches full_name in format {module}.{member}."""
    return pytd_utils.MatchesFullName(
        t, full_name, self.module_info.module_name, self.aliases)

  def _is_tuple_base_type(self, t):
    return isinstance(t, pytd.NamedType) and (
        t.name == "tuple" or self._matches_full_name(t, "builtins.tuple") or
        self._matches_full_name(t, "typing.Tuple"))

  def _is_empty_tuple(self, t):
    return isinstance(t, pytd.TupleType) and not t.parameters

  def _is_heterogeneous_tuple(self, t):
    return isinstance(t, pytd.TupleType)

  def _is_callable_base_type(self, t):
    return (isinstance(t, pytd.NamedType) and
            (self._matches_full_name(t, "typing.Callable") or
             self._matches_full_name(t, "collections.abc.Callable")))

  def _is_literal_base_type(self, t):
    return isinstance(t, pytd.NamedType) and (
        self._matches_full_name(t, "typing.Literal") or
        self._matches_full_name(t, "typing_extensions.Literal"))

  def _parameterized_type(self, base_type, parameters):
    """Return a parameterized type."""
    if self._is_literal_base_type(base_type):
      return types.pytd_literal(parameters)
    elif any(isinstance(p, types.Constant) for p in parameters):
      parameters = ", ".join(
          p.repr_str() if isinstance(p, types.Constant) else "_"
          for p in parameters)
      raise ParseError(
          "%s[%s] not supported" % (pytd_utils.Print(base_type), parameters))
    elif pytdgen.is_any(base_type):
      return pytd.AnythingType()
    elif len(parameters) == 2 and parameters[-1] is self.ELLIPSIS and (
        not self._is_callable_base_type(base_type)):
      element_type = parameters[0]
      if element_type is self.ELLIPSIS:
        raise ParseError("[..., ...] not supported")
      return pytd.GenericType(base_type=base_type, parameters=(element_type,))
    else:
      parameters = tuple(pytd.AnythingType() if p is self.ELLIPSIS else p
                         for p in parameters)
      if self._is_tuple_base_type(base_type):
        return pytdgen.heterogeneous_tuple(base_type, parameters)
      elif self._is_callable_base_type(base_type):
        return pytdgen.pytd_callable(base_type, parameters)
      else:
        assert parameters
        return pytd.GenericType(base_type=base_type, parameters=parameters)

  def resolve_type(self, name: Union[str, pytd_node.Node]) -> pytd_node.Node:
    """Return the fully resolved name for an alias.

    Args:
      name: The name of the type or alias.

    Returns:
      A pytd.NamedType with the fully resolved and qualified name.
    """
    if isinstance(name, (pytd.GenericType, pytd.AnythingType)):
      return name
    if isinstance(name, pytd.NamedType):
      name = name.name
    if name == "nothing":
      return pytd.NothingType()
    base_type = self.type_map.get(name)
    if base_type is None:
      module, dot, tail = name.partition(".")
      full_name = self.module_path_map.get(module, module) + dot + tail
      base_type = pytd.NamedType(full_name)
    return base_type

  def new_type(
      self,
      name: Union[str, pytd_node.Node],
      parameters: Optional[List[pytd_node.Node]] = None
  ) -> pytd_node.Node:
    """Return the AST for a type.

    Args:
      name: The name of the type.
      parameters: List of type parameters.

    Returns:
      A pytd type node.

    Raises:
      ParseError: if the wrong number of parameters is supplied for the
        base_type - e.g., 2 parameters to Optional or no parameters to Union.
    """
    base_type = self.resolve_type(name)
    if not isinstance(base_type, pytd.NamedType):
      # We assume that all type parameters have been defined. Since pytype
      # orders type parameters to appear before classes and functions, this
      # assumption is generally safe. AnyStr is special-cased because imported
      # type parameters aren't recognized.
      type_params = self.type_params + [pytd.TypeParameter("typing.AnyStr")]
      base_type = base_type.Visit(_InsertTypeParameters(type_params))
      try:
        resolved_type = visitors.MaybeSubstituteParameters(
            base_type, parameters)
      except ValueError as e:
        raise ParseError(str(e)) from e
      if resolved_type:
        return resolved_type
    if parameters is not None:
      if (len(parameters) > 1 and isinstance(base_type, pytd.NamedType) and
          base_type.name == "typing.Optional"):
        raise ParseError("Too many options to %s" % base_type.name)
      return self._parameterized_type(base_type, parameters)
    else:
      if (isinstance(base_type, pytd.NamedType) and
          base_type.name in _TYPING_SETS):
        raise ParseError("Missing options to %s" % base_type.name)
      return base_type

  def build_class(
      self, class_name, bases, keywords, decorators, defs
  ) -> pytd.Class:
    """Build a pytd.Class from definitions collected from an ast node."""
    parents, namedtuple_index = classdef.get_parents(bases)
    metaclass = classdef.get_metaclass(keywords, parents)
    constants, methods, aliases, slots, classes = _split_definitions(defs)

    # Make sure we don't have duplicate definitions.
    classdef.check_for_duplicate_defs(methods, constants, aliases)

    # Generate a NamedTuple proxy base class if needed
    if namedtuple_index is not None:
      namedtuple_parent = self.new_named_tuple(
          class_name, [(c.name, c.type) for c in constants])
      parents[namedtuple_index] = namedtuple_parent
      constants = []

    if aliases:
      vals_dict = {val.name: val
                   for val in constants + aliases + methods + classes}
      for val in aliases:
        name = val.name
        seen_names = set()
        while isinstance(val, pytd.Alias):
          if isinstance(val.type, pytd.NamedType):
            _, _, base_name = val.type.name.rpartition(".")
            if base_name in seen_names:
              # This happens in cases like:
              # class X:
              #   Y = something.Y
              # Since we try to resolve aliases immediately, we don't know what
              # type to fill in when the alias value comes from outside the
              # class. The best we can do is Any.
              val = pytd.Constant(name, pytd.AnythingType())
              continue
            seen_names.add(base_name)
            if base_name in vals_dict:
              val = vals_dict[base_name]
              continue
          # The alias value comes from outside the class. The best we can do is
          # to fill in Any.
          val = pytd.Constant(name, pytd.AnythingType())
        if isinstance(val, function.NameAndSig):
          val = dataclasses.replace(val, name=name)
          methods.append(val)
        else:
          if isinstance(val, pytd.Class):
            t = pytdgen.pytd_type(pytd.NamedType(class_name + "." + val.name))
          else:
            t = val.type
          constants.append(pytd.Constant(name, t))

    parents = [p for p in parents if not isinstance(p, pytd.NothingType)]
    methods = function.merge_method_signatures(methods)
    if not parents and class_name not in ["classobj", "object"]:
      # A parent-less class inherits from classobj in Python 2 and from object
      # in Python 3. typeshed assumes the Python 3 behavior for all stubs, so we
      # do the same here.
      parents = (pytd.NamedType("object"),)

    return pytd.Class(name=class_name, metaclass=metaclass,
                      parents=tuple(parents),
                      methods=tuple(methods),
                      constants=tuple(constants),
                      classes=tuple(classes),
                      decorators=tuple(decorators),
                      slots=slots,
                      template=())

  def build_type_decl_unit(self, defs) -> pytd.TypeDeclUnit:
    """Return a pytd.TypeDeclUnit for the given defs (plus parser state)."""
    # defs contains both constant and function definitions.
    constants, functions, aliases, slots, classes = _split_definitions(defs)
    assert not slots  # slots aren't allowed on the module level

    # TODO(mdemello): alias/constant handling is broken in some weird manner.
    # assert not aliases # We handle top-level aliases in add_alias_or_constant
    # constants.extend(self.constants)

    if self.module_info.module_name == "builtins":
      constants.extend(types.builtin_keyword_constants())

    generated_classes = sum(self.generated_classes.values(), [])

    classes = generated_classes + classes
    functions = function.merge_method_signatures(functions)

    name_to_class = {c.name: c for c in classes}
    name_to_constant = {c.name: c for c in constants}
    aliases = []
    for a in self.aliases.values():
      t = _maybe_resolve_alias(a, name_to_class, name_to_constant)
      if t is None:
        continue
      elif isinstance(t, pytd.Function):
        functions.append(t)
      elif isinstance(t, pytd.Constant):
        constants.append(t)
      else:
        assert isinstance(t, pytd.Alias)
        aliases.append(t)

    all_names = ([f.name for f in functions] +
                 [c.name for c in constants] +
                 [c.name for c in self.type_params] +
                 [c.name for c in classes] +
                 [c.name for c in aliases])
    duplicates = [name
                  for name, count in collections.Counter(all_names).items()
                  if count >= 2]
    if duplicates:
      raise ParseError(
          "Duplicate top-level identifier(s): " + ", ".join(duplicates))

    properties = [x for x in functions if x.kind == pytd.PROPERTY]
    if properties:
      prop_names = ", ".join(p.name for p in properties)
      raise ParseError(
          "Module-level functions with property decorators: " + prop_names)

    return pytd.TypeDeclUnit(name=None,
                             constants=tuple(constants),
                             type_params=tuple(self.type_params),
                             functions=tuple(functions),
                             classes=tuple(classes),
                             aliases=tuple(aliases))


def finalize_ast(ast: pytd.TypeDeclUnit):
  ast = ast.Visit(_PropertyToConstant())
  ast = ast.Visit(_InsertTypeParameters(ast.type_params))
  ast = ast.Visit(_VerifyMutators())
  return ast
