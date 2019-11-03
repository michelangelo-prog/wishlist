from flask_restful import Resource

class HelloWorldEndpoint(Resource):
    def get(self):
        return "Hello World"
