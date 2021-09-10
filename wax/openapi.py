import re
from wax.schema import to_json_schema
from aiohttp.web import json_response


def make_operation_id(method, path):
    return ''.join(re.findall('[a-z0-9]+', f'{method} {path}'.lower()))


def real_dict(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


def real_list(*args):
    return [item for item in args if item is not None]


def to_openapi_path(endpoint_dsl) -> dict:
    path = endpoint_dsl['path']
    method = endpoint_dsl['method'].lower()
    endpoint_obj = {
        'operationId': make_operation_id(method, path),
        'tags': [],
        **real_dict(
            summary = endpoint_dsl.get('summary'),
            description = endpoint_dsl.get('description'),
        ),
        'responses': {}
    }
    if endpoint_dsl.get('requestParam'):
        parameters = []
        for params_in, params_dsl in endpoint_dsl['requestParam'].items():
            params_json_schema = to_json_schema(params_dsl)
            for param_name, param_schema in params_json_schema['properties'].items():
                param = {
                    'schema': param_schema,
                    'in': params_in,
                    'name': param_name,
                    'description': params_json_schema.get('description', '')
                }
                if param_name in params_json_schema.get('required', []):
                    param['required'] = True
                parameters.append(param)
        endpoint_obj['parameters'] = parameters
    if endpoint_dsl.get('requestBody'):
        content_type = endpoint_dsl['requestBody'].get('contentType', 'application/json')
        endpoint_obj['requestBody'] = {
            'content': {
                content_type: {
                    'schema': to_json_schema(endpoint_dsl['requestBody']['schema'])
                }
            }
        }
    if endpoint_dsl.get('response'):
        for status_code, status_dsl in endpoint_dsl['response'].items():
            content_type = status_dsl.get('contentType', 'application/json')
            endpoint_obj['responses'][status_code] = {
                'content': {
                    content_type: {
                        'schema': to_json_schema(status_dsl['schema'])
                    }
                }
            }
    return {path: {method: endpoint_obj}}


class GlobalOpenAPI:
    data: dict = {
        'openapi': '3.0.0',
        'info': {
            'title': 'wax-api',
            'version': '1.0'
        },
        'paths': {},
        'components': {
            'schemas': {}
        },
    }

    @classmethod
    def add_endpoint(cls, endpoint_dsl):
        openapi_path = to_openapi_path(endpoint_dsl)
        for path, path_obj in openapi_path.items():
            cls.data['paths'].setdefault(path, {})
            for method, endpoint_obj in path_obj.items():
                cls.data['paths'][path][method] = endpoint_obj


async def show_openapi(requests):
    return json_response(GlobalOpenAPI.data)
