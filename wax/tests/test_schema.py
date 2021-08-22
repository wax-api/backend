"""
Copyright (c) 2021  Chongqing Parsec Inc.
wax-backend is licensed under the Lesspl Public License(v0.2).
You may obtain a copy of Lesspl Public License(v0.2) at: http://www.lesspl.org
"""


from unittest import TestCase
from wax.schema import to_json_schema


class TestSchema(TestCase):
    def test_success(self):
        # 简单类型/字符串
        wax_schema = ["string", {"minLength": 2, "maxLength": 4}]
        json_schema = {
            "type": "string",
            "minLength": 2,
            "maxLength": 4,
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 简单类型/数值
        wax_schema = ["number", {"multipleOf": 10}]
        json_schema = {
            "type": "number",
            "multipleOf": 10,
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 简单类型/布尔
        wax_schema = "boolean"
        json_schema = {"type": "boolean"}
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 简单类型/空值
        wax_schema = "null"
        json_schema = {"type": "null"}
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 复合类型-数组
        wax_schema = ["number", {"array": True}]
        json_schema = {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 复合类型-对象
        wax_schema = {
            "name": "string",
            "age": "integer",
            "address": {
                "city": "string",
                "country": "string"
            }
        }
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "address": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "country": {"type": "string"}
                    }
                }
            }
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        wax_schema = {
            "/^S_/": "string",
            "/^I_/": "integer"
        }
        json_schema = {
            "type": "object",
            "patternProperties": {
                "^S_": {"type": "string"},
                "^I_": {"type": "integer"}
            }
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        wax_schema = [
            {
                "name": "string",
                "age": ["integer", {"required": True}],
                "credit_card": ["string", {"dependencies": ["name"]}]
            },
            {"minProperties": 2, "maxProperties": 3}
        ]
        json_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "credit_card": {"type": "string"}
            },
            "required": ["age"],
            "dependencies": {"credit_card": ["name"]},
            "minProperties": 2,
            "maxProperties": 3
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # Union类型
        wax_schema = ["string", {"canBeArray": True}]
        json_schema = {
            "type": [
                "array",
                "string"
            ],
            "items": {
                "type": "string"
            }
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 复杂结构-引用
        wax_schema = {
            "billing_address": "#Address",
            "shipping_address": "#Address"
        }
        json_schema = {
            "type": "object",
            "properties": {
                "billing_address": {"$ref": "#/components/schemas/Address"},
                "shipping_address": {"$ref": "#/components/schemas/Address"}
            }
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 通用关键字-enum
        wax_schema = ["string", {"enum": ["red", "green", "blue"]}]
        json_schema = {
            "type": "string",
            "enum": ["red", "green", "blue"]
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        wax_schema = ["integer", {"enum": {"0": "OFF", "1": "ON"}}]
        json_schema = {
            "type": "integer",
            "enum": [0, 1],
            "description": "0=OFF 1=ON"
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 通用关键字-description
        wax_schema = ["string", "person name"]
        json_schema = {
            "type": "string",
            "description": "person name"
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        # 简洁形式
        wax_schema = {"key[]": "integer"}
        json_schema = {
            "type": "object",
            "properties": {
                "key": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                }
            }
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        wax_schema = {"key!": "integer"}
        json_schema = {
            "type": "object",
            "properties": {
                "key": {
                    "type": "integer"
                }
            },
            "required": ["key"]
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
        wax_schema = {"key[]!": "integer"}
        json_schema = {
            "type": "object",
            "properties": {
                "key": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                }
            },
            "required": ["key"]
        }
        self.assertDictEqual(to_json_schema(wax_schema), json_schema)
