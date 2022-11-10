# Create and Deploy an API
## presented by Edwin D and Spencer S

### Virtual Environment Discussion
AWS Lambda only supports Python Versions up to to 3.9. As of such, our Python environment has to be 3.9. There are various ways to handle this, it just all depends on whether or not we want to install Brew. 


### The most basic Flask program
```
# save this as app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
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

### Enable AdminGuard
Log into Self Service and enable Admin Guard. 
This will allow you to install AWS CLI. You can then proceed to downloading the AWS CLI Package.

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

### Implement virtual environment