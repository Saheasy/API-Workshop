# Create and Deploy an API

### Enable VPN if you haven't already
Reminder to start recording

### Enable AdminGuard
Log into Self Service and enable Admin Guard. 
This will allow you to install software. 

### Virtual Environment Discussion
AWS Lambda only supports Python Versions up to to 3.9. As of such, our Python environment has to be 3.9. There are various ways to handle this, so I am choosing to use pyenv. 
Install brew   
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`  
Then we install pyenv using brew.   
`brew install pyenv`  
`echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc`  
`echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc`  
`echo 'eval "$(pyenv init -)"' >> ~/.zshrc`  
`exec "$SHELL"`  

We aren't really picky on what Python version we use, as long as it supports Lambda. So I am choosing 3.9.7
` pyenv install 3.9.7`
`pyenv local 3.9.7`
Now that our version is correct, we can run our Virtual Environment as per normal. 
In VSCode, run `python3 venv venv` then `source venv/bin/activate`  
We can now install our dependencies

`pip3 install python-dotenv flask-restful zappa boto3`

## Creating Flask Application
Here is the [Flask RESTful documentation](https://flask-restful.readthedocs.io/en/latest/index.html) that we are referencing
Make sure your main python file is in a python file named "app.py"
### The most basic Flask program
```
# save this as app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```
If you go to [`localhost:5000`](http://localhost:5000) you will see your "Hello, World"

## Our Flask Application
With the Argument parsing and some error handling. This is the final code. 
Curl Commands:
curl localhost:5000/apprentices => GET list of all apprentices
curl localhost:5000/apprentices/3 -d '{"name": "Will Harris", "group": "protozoic"}' -X POST -v -H "Content-Type: application/json" => POST new apprentice
curl localhost:5000/apprentices/3 -d '{"name": "William Harris", "group": "protozoic"}' -X PUT -v -H "Content-Type: application/json" => PUT new changes to apprentice
curl localhost:5000/apprentices/3 -X DELETE -v => DELETE individual apprentice by id
```
# import relevant modules
from flask import Flask
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

# We only need this for local development.
if __name__ == '__main__':
    app.run()
```



## Deploying your Flask Application to the Cloud
I am using [Zappa](https://github.com/zappa/Zappa) to deploy the Flask code to the AWS Cloud. Zappa will set everything up in Lambda and API Gateway.   
Does Pearson use Zappa? Not that I know of, but it operates very similarly to AWS Serverless Application Model which Pearson employees such as Jonathon Morris have used.    
As a heads up, Zappa doesn't work on Python 3.10, but does on 3.9 and below. This is because AWS Lambda doesn't run Python 3.10.    
There are various way to get a 3.9 Python Intepreter running, however I just installed Python 3.9.    
There are tools such as pyenv, pipenv, and so on, but those require having Brew installed. AWS SAM also requires having Brew installed as an fyi.   


Things that we need to do before we can run 'zappa init':

- Install the AWS CLI
- Start an A Cloud Guru AWS Sandbox to grab the secrets
- Store secrets in both the credentials and in a .env
- Setup a virtual environment with Python3.9 in your VSCode

### Install AWS CLI
[Amazon's Tutorial on installing the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

1. Download and install the [AWS CLI package](https://awscli.amazonaws.com/AWSCLIV2.pkg)
2. Run your downloaded file and follow the instructions
   - You can install to any folder, or choose the recommended default folder of /usr/local/aws-cli.
   - The installer automatically creates a symlink at /usr/local/bin/aws that links to the main program in the installation folder you chose.
3. To verify that the shell can find and run the aws command in your `$PATH`, use the following commands.
```
$ which aws
/usr/local/bin/aws 
$ aws --version
aws-cli/2.7.24 Python/3.8.8 Darwin/18.7.0 botocore/2.4.5
```
### Get credentials from A Cloud Guru's AWS Playground
1. Go to [A Cloud Guru's AWS Playground](https://learn.acloud.guru/cloud-playground/cloud-sandboxes)'s webpage
2. Start the AWS Playground to see the Access Key ID and Secret Access Key
3. In an .env file insert the credentials like so: 
```
AWS_ACCESS_KEY_ID=InsertAccessKeyIDHere
AWS_SECRET_ACCESS_KEY=InsertSecretAccessKeyHere
AWS_DEFAULT_REGION=us-east-1
```
4. In your Terminal use the AWS CLI console to add your credentials: (This will prompt line by line) 
```
$ aws configure --profile AGC-credentials
AWS Access Key ID [None]: AKIAI44QH8DHBEXAMPLE
AWS Secret Access Key [None]: je7MtGbClwBF/2Zp9Utk/h3yCo8nvbEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: text
```

Create a new file called aws_objects.py and insert this code 

```
#Import the AWS SDK for Python
import boto3

#This is class with all of the AWS oriented code
class apiAWS:
    def __init__(self, profile_name, table_name):
        # Create a Session with the profile that has our A Cloud Guru Credentials
        self.session = boto3.Session()

        # Create a DynamoDB client and resource using the A Cloud Guru session 
        # Client and Resource do some of the same things, but some of the functions are exclusive to each other 
        # Overall we try to use Resource when we can 
        self.dynamodb_client = self.session.client('dynamodb', region_name='us-east-1')
        self.dynamodb = self.session.resource('dynamodb', region_name='us-east-1')

        ''' A List Comprehension that puts this code into a single line:
        table = []
        for db in self.dynamodb_client.list_tables()['TableNames']:
            if db == table_name:
                table.append(db)
        '''
        my_table = [ db for db in self.dynamodb_client.list_tables()['TableNames'] if db == table_name ]

        # If there isn't anything in the list, then we need to create one. 
        if my_table == []:
            self.create(table_name)

        # Assigned table to class variable
        self.table = self.dynamodb.Table(table_name)
        print(self.table)

    def create(self, table_name):
        # We create the table. It needs an unique key, which is what full_name is
        # Provisioned Throughput is the amount of requests it can handle in a second
        self.table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'full_name',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                
                {
                    'AttributeName': 'full_name',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 100,
                'WriteCapacityUnits': 100
            }
        )

        # Wait until the table exists.
        self.table.wait_until_exists()
        
    def info(self):
        #Just to see what is in the table
        return self.table.scan()['Items']

    def post_data(self, full_name, nickname, group, location):
        # This is the equilivant of a post request, as it overwrites everything that's assigned to the 'full_name'
        self.table.put_item(
            Item={
                'full_name':full_name,
                'nickname':nickname,
                'group':group,
                'location': location
            })

    #https://stackoverflow.com/questions/63497448/dynamodb-update-multiple-values
    # This is a wee bit overcomplicated so I recommend reading this StackOverFlow article
    # In order to not overwrite everything, we need to use the update command
    # This function could have a workshop of it's own, but we just want to write data without delete the other values in our database
    # There is a way to write a bunch of updates at once without calling the function multiple times but it gets a wee bit complicated
    def put_data(self, full_name, key, value):
        self.table.update_item(
            Key={'full_name':full_name},
            UpdateExpression= f'SET #KEY = :value',
            ExpressionAttributeNames={ '#KEY':key},
            ExpressionAttributeValues={ ':value':value  }
        )
    
    #This fetches the data of whatever key is entered 
    def get_data(self, full_name):
        return self.table.get_item(Key={'full_name':full_name} )['Item']

    #This deletes the key and data of whatever key is entered
    def delete_data(self, full_name):
        self.table.delete_item(Key={'full_name':full_name})

    #This deletes the entire table. Is not in the RESTFUL API
    def delete_table(self): 
        self.table.delete()
```

And between the last add_resource function and the `if __name__ == "__main__"` insert this code:
```
# Flask API with DynamoDB
# Initialized the apiAWS class, which checks for/creates a dynamodb
aws = apiAWS('AGC-credentials', 'API_Project')

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

```

We should click run to see if everything works as it should on our local machine. Then we can deploy the file via Zappa.    
`zappa init`

You should fill out as following:  
What do you want to call this environment (default 'dev'): `dev`  
We found the following profiles: default, and AGC-credentials. Which would you like us to use? (default 'default'): `AGC-credentials`  
What do you want to call your bucket? (default 'zappa-5jpmga1hm'): `zappa-5jpmga1hm-api-workshop`  
I choose the default name, then add a descriptive term at the end. Because all S3 buckets need to be unique, this helps it be unique.   
Where is your app's function? (default 'app.app'): `app.app`  
Would you like to deploy this application globally? (default 'n') [y/n/(p)rimary]: `n`  
Does this look okay? (default 'y') [y/n]: `y`  

From here we can run: `zappa deploy dev` and it should work. If we want to make any changes, then we should run `zappa update dev`

While we wait for this to deploy, Spencer will explain the DynamoDB code. 