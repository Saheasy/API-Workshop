# import relevant modules
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort

# create Flask app
app = Flask(__name__)

# create API object
api = Api(app)

# Basic Flask API #
# create 'database'
apprentices = {
            1: {"name": "Edwin Duggirala", "group": "protozoic"},
            2: {"name": "Spencer Sahu", "group": "protzoic"}
        }

apprentice_POST_args = reqparse.RequestParser()
apprentice_POST_args.add_argument("name", type = str, help = "Name is required.", required = True)
apprentice_POST_args.add_argument("group", type = str, help = "Name is required.", required = True)

apprentice_PUT_args = reqparse.RequestParser()
apprentice_PUT_args.add_argument("name", type = str)
apprentice_PUT_args.add_argument("group", type = str)


# create class for only the list of apprentices
class apprentice_list(Resource):

    def get(self):
        return apprentices


# create class for apprentice, make it a resource, get all data on apprentices
class apprentice(Resource):  

    def get(self, apprentice_id):
        return apprentices[apprentice_id]

    def post(self, apprentice_id):
        args = apprentice_POST_args.parse_args()
        if apprentice_id in apprentices:
            abort(409, "Apprentice information already exists")
        apprentices[apprentice_id] = {"name": args["name"], "group": args["group"]}
        return apprentices[apprentice_id]

    def put(self, apprentice_id):
        args = apprentice_PUT_args.parse_args()
        if apprentice_id not in apprentices:
            abort(404, message = "Apprentice does not exist. Cannot update.")
        if args["name"]:
            apprentices[apprentice_id]["name"] = args["name"]
        if args["group"]:
            apprentices[apprentice_id]["group"] = args["group"]
        return apprentices[apprentice_id]

    def delete(self, apprentice_id):
        del apprentices[apprentice_id]
        return apprentices

api.add_resource(apprentice_list, "/apprentices")
api.add_resource(apprentice, "/apprentices/<int:apprentice_id>")



# Flask API with DynamoDB
aws_apprentice_POST_args = reqparse.RequestParser()
aws_apprentice_POST_args.add_argument("name", type = str, help = "Name is required.", required = True)
aws_apprentice_POST_args.add_argument("group", type = str, help = "Name is required.", required = True)

aws_apprentice_PUT_args = reqparse.RequestParser()
aws_apprentice_PUT_args.add_argument("name", type = str)
aws_apprentice_PUT_args.add_argument("group", type = str)


# create class for only the list of apprentices
class AwsApprenticeList(Resource):
    def get(self):
        return apprentices


# create class for apprentice, make it a resource, get all data on apprentices
class AwsApprentice(Resource):  

    def get(self, apprentice_id):
        return apprentices[apprentice_id]

    def post(self, apprentice_id):
        args = apprentice_POST_args.parse_args()
        if apprentice_id in apprentices:
            abort(409, "Apprentice information already exists")
        apprentices[apprentice_id] = {"name": args["name"], "group": args["group"]}
        return apprentices[apprentice_id]

    def put(self, apprentice_id):
        args = apprentice_PUT_args.parse_args()
        if apprentice_id not in apprentices:
            abort(404, message = "Apprentice does not exist. Cannot update.")
        if args["name"]:
            apprentices[apprentice_id]["name"] = args["name"]
        if args["group"]:
            apprentices[apprentice_id]["group"] = args["group"]
        return apprentices[apprentice_id]

    def delete(self, apprentice_id):
        del apprentices[apprentice_id]
        return apprentices

api.add_resource(AwsApprenticeList, "/aws")
api.add_resource(AwsApprentice, "/aws/<int:apprentice_id>")

if __name__ == "__main__":
    app.run(debug=True)