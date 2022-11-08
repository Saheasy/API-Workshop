# import relevant modules
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from aws_objects import apiAWS
from dotenv import load_dotenv
load_dotenv()

# create Flask app
app = Flask(__name__)

# create API object
api = Api(app)

aws = apiAWS('temp-AGC', 'API_Project')

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
        try:
            return apprentices[apprentice_id]
        except:
            abort(404, message="Apprentice ID not in database")

    def post(self, apprentice_id):
        args = apprentice_POST_args.parse_args()
        if apprentice_id in apprentices:
            abort(409, message="Apprentice information already exists")
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
# Initialized the apiAWS class, which checks for/creates a dynamodb

aws_apprentice_POST_args = reqparse.RequestParser()
aws_apprentice_POST_args.add_argument("nickname", type = str, help = "Nickname is required.", required = True)
aws_apprentice_POST_args.add_argument("group", type = str, help = "Pathfinders Group is required.", required = True)
aws_apprentice_POST_args.add_argument("location", type = str)

aws_apprentice_PUT_args = reqparse.RequestParser()
aws_apprentice_PUT_args.add_argument("nickname", type = str)
aws_apprentice_PUT_args.add_argument("group", type = str)
aws_apprentice_PUT_args.add_argument("location", type = str)

# create class for only the list of apprentices
class AwsApprenticeList(Resource):
    def get(self):
        return aws.info()

# create class for apprentice, make it a resource, get all data on apprentices
class AwsApprentice(Resource):  

    def get(self, apprentice_id):
        return aws.get_data(apprentice_id)

    def post(self, apprentice_id):
        args = aws_apprentice_POST_args.parse_args()
        if set(args) != {'nickname', 'group', 'location'}:
            abort(400)
        aws.post_data(apprentice_id, args['nickname'], args['group'], args['location'])
        return args

    def put(self, apprentice_id):
        args = aws_apprentice_PUT_args.parse_args()
        x = [ aws.put_data(apprentice_id, arg, args[arg]) for arg in args if args[arg] != None ]
        print(x)
        return f"Data Inserted {args}"

    def delete(self, apprentice_id):
        aws.delete_data(apprentice_id)
        return f'{apprentice_id} has been deleted'

api.add_resource(AwsApprenticeList, "/aws/")
api.add_resource(AwsApprentice, "/aws/<string:apprentice_id>")


# We only need this for local development.
if __name__ == '__main__':
    app.run()