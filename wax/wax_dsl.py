import json
import jsonschema
from aiohttp.web import Request, Response, json_response, HTTPBadRequest, HTTPInternalServerError
from wax.schema import to_json_schema
from wax.json_util import json_dumps


ENDPOINT_JSON_SCHEMA = to_json_schema({
    "method!": "string",
    "path!": "string",
    "summary": "string",
    "description!": "string",
    "security[]": "string",
    "requestParam": {
        "path": "object",
        "query": "object",
        "header": "object",
        "cookie": "object"
    },
    "requestBody": "object",
    "response": "object",
    "lambdas[]": "string",
})


def wax_validate(instance, *, wax_schema, allow_additional=False):
    json_schema = to_json_schema(wax_schema, allow_additional)
    jsonschema.validate(instance=instance, schema=json_schema, format_checker=jsonschema.draft7_format_checker)


def _cast(value_str, value_type):
    return {'string': str, 'integer': int, 'number': float, 'bool': (lambda x: bool(int(x)))}[value_type](value_str)


def params_cast(params, schemas):
    result = {}
    if not params or not schemas:
        return result
    for key, param_schema in schemas.items():
        if key in params:
            value_str = params[key]
            value_type = param_schema['type']
            result[key] = _cast(value_str, value_type)
    wax_validate(result, wax_schema=schemas)
    return result


def endpoint(endpoint_dsl):
    jsonschema.validate(instance=endpoint_dsl, schema=ENDPOINT_JSON_SCHEMA)

    def wrapper(handler) -> dict:
        async def coro(request: Request):
            request['input'] = {}
            try:
                if request_param_dsl := endpoint_dsl.get('requestParam', {}):
                    request['input']['query'] = params_cast(request.query, request_param_dsl.get('query'))
                    request['input']['path'] = params_cast(request.match_info, request_param_dsl.get('path'))
                    request['input']['header'] = params_cast(request.headers, request_param_dsl.get('header'))
                if request_body_dsl := endpoint_dsl.get('requestBody'):
                    if '/json' in request_param_dsl.get('contentType', 'application/json'):
                        request_data = await request.json()
                        wax_validate(request_data, wax_schema=request_body_dsl['schema'])
                        request['input']['body'] = request_data
            except jsonschema.ValidationError as e:
                raise HTTPBadRequest(text=str(e))
            try:
                response = await handler(request)
            except AssertionError as e:
                raise HTTPBadRequest(text=str(e))
            if not isinstance(response, Response):
                response = json_response(response, dumps=json_dumps)
            try:
                if response_body_dsl := endpoint_dsl.get('response', {}).get(str(response.status)):
                    if '/json' in response_body_dsl.get('contentType', 'application/json'):
                        wax_validate(json.loads(response.text), wax_schema=response_body_dsl['schema'])
            except jsonschema.ValidationError as e:
                raise HTTPInternalServerError(text=str(e))
            return response
        return {'method': endpoint_dsl['method'], 'path': endpoint_dsl['path'], 'handler': coro}
    return wrapper


def input_path(request: Request):
    return request['input'].get('path', {})


def input_query(request: Request):
    return request['input'].get('query', {})


def input_header(request: Request):
    return request['input'].get('header', {})


def input_body(request: Request):
    return request['input'].get('body', None)


class Keys:
    def __init__(self, *keys):
        self.keys = keys

    def __rsub__(self, other):
        if isinstance(other, dict):
            for key in self.keys:
                if '.' in key:
                    key_head, key_tail = key.split('.', 1)
                    if key_head in other:
                        Keys(key_tail).__rsub__(other[key_head])
                else:
                    other.pop(key, None)
        elif isinstance(other, list):
            for item in other:
                if isinstance(item, dict):
                    self.__rsub__(item)
        return other
