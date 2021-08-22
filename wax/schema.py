class WaxSyntaxError(Exception):
    def __init__(self, message):
        super().__init__(message)


def expand_brief_mode(key, schema):
    if key.endswith('!'):
        key = key[:-1]
        schema[2]['required'] = True
    if key.endswith('[]'):
        key = key[:-2]
        schema[2]['array'] = True
    return key, schema


def get_full_wax_schema(wax_schema):
    if isinstance(wax_schema, (str, dict)):
        return [wax_schema, None, {}]
    elif isinstance(wax_schema, list) and len(wax_schema) == 1:
        return [wax_schema[0], None, {}]
    elif isinstance(wax_schema, list) and len(wax_schema) == 2:
        if isinstance(wax_schema[1], dict):
            return [wax_schema[0], None, wax_schema[1]]
        else:
            return [wax_schema[0], wax_schema[1], {}]
    elif isinstance(wax_schema, list) and len(wax_schema) == 3:
        return [wax_schema[0], wax_schema[1], wax_schema[2]]
    else:
        raise WaxSyntaxError(f'invalid schema: {wax_schema}')


def to_json_schema(wax_schema) -> dict:
    """
    把wax_schema转换为json_schema
    wax_schema定义：https://github.com/wax-api/rfcs/blob/main/WSS.8.md
    """
    schema_type, description, schema_extra = get_full_wax_schema(wax_schema)
    if description is not None:
        schema_extra['description'] = description
    if schema_extra.pop('array', False):
        schema_extra['items'] = to_json_schema(schema_type)
        return {'type': 'array', **schema_extra}
    if isinstance(schema_type, dict):
        for dict_key, dict_val in schema_type.items():
            sub_schema = get_full_wax_schema(dict_val)
            dict_key, sub_schema = expand_brief_mode(dict_key, sub_schema)
            sub_json_schema = to_json_schema(sub_schema)
            if len(dict_key) > 2 and dict_key.strip('/') == dict_key[1:-1]:
                properties_key, field_key = 'patternProperties', dict_key[1:-1]
            else:
                properties_key, field_key = 'properties', dict_key
                if sub_json_schema.pop('required', False):
                    schema_extra.setdefault('required', [])
                    schema_extra['required'].append(field_key)
                if dependencies := sub_json_schema.pop('dependencies', None):
                    schema_extra.setdefault('dependencies', {})
                    schema_extra['dependencies'][field_key] = dependencies
            schema_extra.setdefault(properties_key, {})
            schema_extra[properties_key][field_key] = sub_json_schema
        schema_type = 'object'
    # Ref
    if isinstance(schema_type, str) and schema_type.startswith('#'):
        return {'$ref': f'#/components/schemas/{schema_type[1:]}'}
    # Enum
    if enum_value := schema_extra.pop('enum', None):
        caster = int if schema_type == 'integer' else str
        if isinstance(enum_value, dict):
            schema_extra['enum'] = list(map(caster, enum_value.keys()))
            schema_extra['description'] = ' '.join([
                schema_extra.get('schema_extra', ''),
                *[f'{k}={v}' for k, v in enum_value.items()]
            ]).strip()
        else:
            schema_extra['enum'] = list(map(caster, enum_value))
    # Union
    if schema_extra.pop('canBeArray', False):
        return {
            'type': ['array', schema_type],
            'items': {'type': schema_type, **schema_extra}
        }
    else:
        return {'type': schema_type, **schema_extra}
