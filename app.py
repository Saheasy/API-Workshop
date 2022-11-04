# app.py
from my_requests import data_spencer
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class TodoSimple(Resource):
    def __init__(self):
        self.data = {
            "spencer_sahu": {
                "first_name": "Spencer",
                "last_name": "Sahu",
                "nickname": "Duck",
                "pathfinders_group": "Protozoic",
                "location":"Iowa City"
            },
            "edwin_duggirala": {
                "first_name": "Edwin",
                "last_name": "Duggirala",
                "nickname": "Edlose",
                "pathfinders_group": "Protozoic",
                "location":"San Antonio"
            }
        }
        self.spencer = data_spencer
    def get(self):
        return self.data

    def put(self, id):
        self.data[id] = request.form['data']
        return self.data

    def post(self, id):
        self.data[id] = request.form['data']
        return self.data

    def delete(self, id):
        del self.data[id]
        return self.data

api.add_resource(TodoSimple,'/<string:id>')

# We only need this for local development.
if __name__ == '__main__':
 app.run()