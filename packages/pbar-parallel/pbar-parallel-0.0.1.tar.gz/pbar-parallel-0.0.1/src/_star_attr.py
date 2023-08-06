"""Code by https://gist.github.com/oakkitten/03ca8f9c1113a7e32e32135e2cf5fef9
"""


import inspect
from contextlib import suppress
from functools import wraps
import typing

import attr

META_STAR_ARG = "__star_arg"


def omittable_parentheses(maybe_decorator=None, /, allow_partial: bool=False):      # noqa
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if allow_partial:
                if args and callable(args[-1]):
                    *args, fu = args
                    return func(*args, **kwargs)(fu)
            elif len(args) == 1 and callable(args[-1]) and not kwargs:
                return func()(args[0])
            return func(*args, **kwargs)
        return wrapper
    return decorator if maybe_decorator is None else decorator(maybe_decorator)


def star_attrib(*args, **kwargs):
    result = attr.attrib(*args, **kwargs)
    if result._default is not attr.NOTHING:      # noqa
        raise ValueError("Star attribute can't have a default value")
    if not result.init:
        raise ValueError("Star attribute must not have init=False")
    result.metadata[META_STAR_ARG] = True
    return result


def is_star_field(attribute):
    return attribute.metadata.get(META_STAR_ARG, False)


# this removes annotations so that we can simply `str()` the new signature. otherwise, we would have to get the
# namespace with stuff like {"Optional": typing.Optional} from somewhere. we can just use `__annotations__` for this
def adjust_parameters(parameters, star_param_name=None, star_keyword_param_name=None):
    yield_last = None
    for param in parameters:
        param = param.replace(annotation=inspect.Signature.empty)
        if param.name == star_param_name:
            yield param.replace(kind=inspect.Parameter.VAR_POSITIONAL)
        elif param.name == star_keyword_param_name:
            yield_last = param.replace(kind=inspect.Parameter.VAR_KEYWORD)
        else:
            yield param
    if yield_last:
        yield yield_last


# returns foo from Tuple[foo, ...] or Sequence[str]
def get_star_field_annotation_argument(annotation):
    origin, arguments = typing.get_origin(annotation), typing.get_args(annotation)
    if inspect.isclass(origin):
        if origin is tuple:
            if len(arguments) == 2 and arguments[1] is ...:
                return arguments[0]
        elif issubclass(tuple, origin) and len(arguments) == 1:
            return arguments[0]
    raise LookupError


# returns foo from Dict[str, foo]
def get_star_keyword_field_annotation_argument(annotation):
    origin, arguments = typing.get_origin(annotation), typing.get_args(annotation)
    if inspect.isclass(origin) and issubclass(dict, origin) and len(arguments) == 2 and arguments[0] is str:
        return arguments[1]
    raise LookupError


# get_type_hints() seems to be not working on cls.__init__ but works on cls itself. __init__'s parameters can differ
# slightly, e.g. in case of a converter the annotation is not present
def get_evaluated_annotation(cls, name):
    try:
        original_annotations = cls.__annotations__
        cls.__annotations__ = {name: cls.__init__.__annotations__[name]}
        annotation = typing.get_type_hints(cls)[name]
        cls.__annotations__ = original_annotations
    except Exception:   # noqa
        annotation = None
    return annotation


def starrify_class(cls):
    original_signature = inspect.signature(cls.__init__)
    init_fields = [field for field in attr.fields(cls) if field.init]

    star_field_name = star_keyword_field_name = None
    original_annotations = cls.__init__.__annotations__
    annotations = {"return": None}

    for field in init_fields:
        name = field.name
        if is_star_field(field):
            if field.kw_only:
                if star_keyword_field_name:
                    raise ValueError("Too many star keyword attributes")
                star_keyword_field_name = name
                with suppress(LookupError):
                    annotations[name] = get_star_keyword_field_annotation_argument(
                            get_evaluated_annotation(cls, name))
            else:
                if star_field_name:
                    raise ValueError("Too many star attributes")
                star_field_name = name
                with suppress(LookupError):
                    annotations[name] = get_star_field_annotation_argument(
                            get_evaluated_annotation(cls, name))
        else:
            with suppress(KeyError):
                annotations[name] = original_annotations[name]

    new_signature = original_signature.replace(parameters=list(adjust_parameters(
            original_signature.parameters.values(), star_field_name, star_keyword_field_name)))
    pass_through_arguments = ", ".join(f"{field.name}={field.name}" for field in init_fields)

    code = (f"def __init__{new_signature}:\n"
            f"    original_init(self, {pass_through_arguments})")

    namespace = dict(NOTHING=attr.NOTHING, original_init=cls.__init__)
    eval(compile(code, filename="", mode="exec"), namespace)
    __init__ = namespace["__init__"]
    __init__.__annotations__ = annotations
    cls.__init__ = __init__


@omittable_parentheses(allow_partial=True)
def star_attrs(*args, **kwargs):
    def decorator(cls):
        cls = attr.attrs(*args, **kwargs)(cls)
        starrify_class(cls)
        return cls
    return decorator