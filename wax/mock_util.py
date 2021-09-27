from aiohttp.web import Request, Response
from aiohttp.web import Request, Response, json_response, HTTPBadRequest, HTTPInternalServerError, HTTPNotFound, HTTPMethodNotAllowed
import json
import jsonschema
import re
from wax.inject_util import get_request_ctx
from wax.schema import to_json_schema
from wax.wax_dsl import params_cast
from wax.mapper.interface import InterfaceMapper
from wax.mapper.mock import MockMapper
from wax.mapper.entity import EntityMapper


def re_standardize(pattern: str) -> str:
    """
        >>> pattern = re_standardize('/add/{x}/{y}')
        >>> pattern
        '^/add/(?P<x>[^/]+)/(?P<y>[^/]+)$'
        >>> re.search(pattern, '/add/234/5').groupdict()
        {'x': '234', 'y': '5'}
        >>> re.search(pattern, '/add//add') is None
        True
        >>> re.search(pattern, '/add/1/2/') is None
        True

    """
    if not pattern:
        return '^$'
    if pattern[0] != '^':
        pattern = '^' + pattern
    if pattern[-1] != '$':
        pattern = pattern + '$'
    def _repl(obj):
        x = obj.groups()[0]
        return '(?P<%s>[^/]+)' % x

    return re.sub(r'\{([^0-9].*?)\}', _repl, pattern)


def wax_validate(instance, *, wax_schema, resolver, allow_additional=False):
    json_schema = to_json_schema(wax_schema, allow_additional)
    jsonschema.validate(instance=instance, schema=json_schema, resolver=resolver, format_checker=jsonschema.draft7_format_checker)


def hit_endpoint(interface_list, method, realpath):
    allowed_methods = []
    for interface in interface_list:
        search_ret = re.compile(re_standardize(interface['path'])).search(realpath)
        if search_ret:
            if interface['method'] != method:
                allowed_methods.append(interface['method'])
            else:
                return interface['iid'], search_ret.groupdict()
    if allowed_methods:
        raise HTTPMethodNotAllowed(method, allowed_methods)
    else:
        raise HTTPNotFound


async def mock_dealer(request: Request) -> Response:
    interface_mapper = get_request_ctx(request, InterfaceMapper, 'interface_mapper')
    mock_mapper = get_request_ctx(request, MockMapper, 'mock_mapper')
    entity_mapper = get_request_ctx(request, EntityMapper, 'entity_mapper')
    # 1.找到interface
    project_id = int(request.match_info['project_id'])
    path_info = '/' + request.match_info['path_info']
    interface_list = await interface_mapper.select_list(project_id=project_id)
    interface_iid, path_dict = hit_endpoint(interface_list, request.method, path_info)
    endpoint_dsl = (await interface_mapper.select_by_iid(project_id=project_id, iid=interface_iid))['endpoint']
    # 2. 找到entity转换成resolver
    entity_list = await entity_mapper.select_list(project_id=project_id)
    resolver = {'components': {'schemas': {}}}
    for entity in entity_list:
        entity_name = entity['name']
        entity_schema = to_json_schema(entity['content'], allow_additional=False)
        resolver['components']['schemas'][entity_name] = entity_schema
    # 3. 参数校验
    try:
        if request_param_dsl := endpoint_dsl.get('requestParam', {}):
            query_input = params_cast(request.query, request_param_dsl.get('query'))
            path_input = params_cast(path_dict, request_param_dsl.get('path'))
            header_input = params_cast(request.headers, request_param_dsl.get('header'))
        if request_body_dsl := endpoint_dsl.get('requestBody'):
            if '/json' in request_param_dsl.get('contentType', 'application/json'):
                request_data = await request.json()
                wax_validate(request_data, wax_schema=request_body_dsl['schema'], resolver=resolver)
    except jsonschema.ValidationError as e:
        raise HTTPBadRequest(text=str(e))
    # 4.找到active mock
    mock_db = await mock_mapper.select_by_active(project_id=project_id, interface_iid=interface_iid)
    if not mock_db:
        raise HTTPInternalServerError(text='No active mock!')
    response_status = mock_db['status_code']
    response_data = json.loads(mock_db['content'])
    # 5.返回结果
    try:
        if response_body_dsl := endpoint_dsl.get('response', {}).get(response_status):
            if '/json' in response_body_dsl.get('contentType', 'application/json'):
                wax_validate(response_data, wax_schema=response_body_dsl['schema'], resolver=resolver)
    except jsonschema.ValidationError as e:
        raise HTTPInternalServerError(text=str(e))
    if mock_db['headers'] and (response_header := json.loads(mock_db['headers'])):
        return json_response(response_data, status=response_status, headers=response_header)
    else:
        return json_response(response_data, status=response_status)
