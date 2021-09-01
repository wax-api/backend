from typing import TypeVar, Type
from aiohttp.web import Request
import inspect
from wax.utils import func_arg_spec


T = TypeVar('T')


def inspect_func_params(request, fn):
    params = {}
    for param_name, (param_type, param_default, param_kind) in func_arg_spec(fn).items():
        if param_name == 'self':
            continue
        if param_type is inspect.Signature.empty:
            raise TypeError(f'inspect failed: {fn.__name__} param {param_name} has no type hint')
        if param_kind != 1 and param_type != 3:
            raise TypeError(f'inspect failed: {fn.__name__} param {param_name} is not keyword type')
        if param_default is not inspect.Signature.empty:
            raise TypeError(f'inspect failed: {fn.__name__} param {param_name} cannot have default value')
        if param_type is Request:
            params[param_name] = request
        else:
            params[param_name] = get_request_ctx(request, type_=param_type, name=param_name)
    return params


def get_request_ctx(request: Request, type_: Type[T], name: str) -> T:
    ctx_name = f'{type_.__name__}:{name}'
    if ctx_name in request:
        return request[ctx_name]
    params = inspect_func_params(request, getattr(type_, '__init__'))
    return type_(**params)


def set_request_ctx(request: Request, type_, name: str, instance):
    ctx_name = f'{type_.__name__}:{name}'
    request[ctx_name] = instance
