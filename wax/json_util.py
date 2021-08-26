import json
from datetime import datetime, date


def _default_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)


def json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, default=_default_serial)
