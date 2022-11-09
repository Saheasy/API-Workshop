# Create and Deploy an API
## presented by Edwin D and Spencer S

### The most basic Flask program
```
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
```

## Deploying your Flask Application to the Cloud
I am using [Zappa](https://github.com/zappa/Zappa) to deploy the Flask code to the AWS Cloud. Zappa will set everything up in Lambda and API Gateway. 
Does Pearson use Zappa? Not that I know of, but it operates very similarly to AWS Serverless Application Model which Pearson employees such as Jonathon Morris have used. 

Things that we need to do before we can run 'zappa init':
- Install the AWS CLI
- 