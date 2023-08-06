"""Apply decorators to classes and functions."""

from typing import Iterable, List, Tuple

from pytype.pytd import base_visitor
from pytype.pytd import pytd
from pytype.pytd.codegen import function


class ValidateDecoratedClassVisitor(base_visitor.Visitor):
  """Apply class decorators."""

  def EnterClass(self, cls):
    validate_class(cls)


def _decorate_class(cls: pytd.Class, decorator: str) -> Tuple[pytd.Class, bool]:
  """Apply a single decorator to a class."""
  factory = _DECORATORS.get(decorator, None)
  if factory:
    return factory(cls), True
  else:
    # do nothing for unknown decorators
    return cls, False


def _validate_class(cls: pytd.Class, decorator: str) -> None:
  """Validate a single decorator for a class."""
  validator = _VALIDATORS.get(decorator, None)
  if validator:
    validator(cls)


def _decorator_names(cls: pytd.Class) -> List[str]:
  return [x.type.name for x in reversed(cls.decorators)]  # pytype: disable=attribute-error


def check_defaults(fields: Iterable[pytd.Constant], cls_name: str):
  """Check that a non-default field does not follow a default one."""
  default = None
  for c in fields:
    if c.value is not None:
      default = c.name
    elif default:
      raise TypeError(
          f"In class {cls_name}: "
          f"non-default argument {c.name} follows default argument {default}")


def check_class(cls: pytd.Class) -> None:
  check_defaults(cls.constants, cls.name)


def add_init_from_fields(
    cls: pytd.Class,
    fields: Iterable[pytd.Constant]
) -> pytd.Class:
  check_defaults(fields, cls.name)
  init = function.generate_init(fields)
  methods = cls.methods + (init,)
  return cls.Replace(methods=methods)


def add_generated_init(cls: pytd.Class) -> pytd.Class:
  return add_init_from_fields(cls, cls.constants)


def process_class(cls: pytd.Class) -> Tuple[pytd.Class, bool]:
  """Apply all decorators to a class."""
  changed = False
  for decorator in _decorator_names(cls):
    cls, decorated = _decorate_class(cls, decorator)
    changed = changed or decorated
  return cls, changed


def validate_class(cls: pytd.Class) -> None:
  for decorator in _decorator_names(cls):
    _validate_class(cls, decorator)


# NOTE: For attrs, the resolved "real name" of the decorator in pyi files is
# attr._make.attrs; the aliases are added here in case the attrs stub files
# change to hide that implementation detail. We also add an implicit
# "auto_attribs=True" to @attr.s decorators in pyi files.

_DECORATORS = {
    "dataclasses.dataclass": add_generated_init,
    "attr.s": add_generated_init,
    "attr.attrs": add_generated_init,
    "attr._make.attrs": add_generated_init,
}


_VALIDATORS = {
    "dataclasses.dataclass": check_class,
    "attr.s": check_class,
    "attr.attrs": check_class,
    "attr._make.attrs": check_class,
}
