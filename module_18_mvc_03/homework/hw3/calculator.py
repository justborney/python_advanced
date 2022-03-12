import json
from werkzeug.wrappers import Response
from jsonrpc import JSONRPCResponseManager, dispatcher
from schemas import InputData
from marshmallow import ValidationError
from flask_restful import Api, Resource
from flask import Flask, request
from flasgger import APISpec, Swagger
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

app = Flask(__name__)
api = Api(app)
spec = APISpec(
    title='JSONRPC Calculator',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)

template = spec.to_flasgger(
    app,
    definitions=[InputData]
)

swagger = Swagger(app, template=template)


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 'Division by zero is not allowed'


class Calculator(Resource):
    def post(self) -> Response:
        """
        Endpoint for counting
        :return: Counting result or mistake description
        ---
        tags:
        - Calculator
        parameters: [
            {
              in: body,
              name: input data,
              schema: {
                $ref: '#/definitions/InputData'
              }
            },
          # {
          #   in: body,
          #   name: method,
          #   description: calculating method,
          #   type: string,
          #   enum: ["add", "subtract", "multiply", "divide"]
          # },
          # {
          #   in: body,
          #   name: params,
          #   description: input int values,
          #   schema: {
          #     type: array,
          #     items: {
          #       type: integer
          #     }
          #   }
          # },
          # {
          #   in: body,
          #   name: jsonrpc,
          #   description: JSONRPC version,
          #   type: integer
          # },
          # {
          #   in: body,
          #   name: id,
          #   description: request id,
          #   type: integer
          # }
        ]
        responses:
          200:
            description: Counting result,
          400:
            description: Wrong input data
        """
        schema = InputData()
        data = request.json
        try:
            schema.load(data)

            dispatcher["add"] = lambda a, b: a + b
            dispatcher["subtract"] = lambda a, b: a - b
            dispatcher["multiply"] = lambda a, b: a * b
            dispatcher["divide"] = lambda a, b: divide(a, b)

            response = JSONRPCResponseManager.handle(request.data, dispatcher)

            return Response(response.json, mimetype='application/json', status=200)

        except ValidationError as exc:
            response = {'result': exc.messages,
                        'jsonrpc': json.loads(request.data)['jsonrpc'],
                        'id': json.loads(request.data)['id']}

            return Response(json.dumps(response), mimetype='application/json', status=400)


api.add_resource(Calculator, '/calc')

if __name__ == '__main__':
    app.run(debug=True)
