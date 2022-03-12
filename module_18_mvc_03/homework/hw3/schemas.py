from typing import Dict
from marshmallow import Schema, fields, validates, ValidationError, post_load

METHODS = ['add', 'subtract', 'multiply', 'divide']


class InputData(Schema):
    method = fields.Str(required=True)
    jsonrpc = fields.Float(required=True)
    id = fields.Int(required=True)
    params = fields.List(fields.Int(required=True))

    @validates('params')
    def validate_params(self, params: list) -> None:
        if len(params) < 2:
            raise ValidationError(
                'Not enough parameters'
            )

    @validates('method')
    def validate_method(self, method) -> None:
        if method not in METHODS:
            raise ValidationError(
                "Wrong method"
            )

    @post_load
    def create_data(self, input_data: Dict, **kwargs) -> Dict:
        return input_data
