import boto3

class apiAWS:
    def __init__(self, profile_name, table_name):
        self.session = boto3.Session(profile_name='temp-AGC')
        self.dynamodb_client = self.session.client('dynamodb', region_name='us-east-1')
        self.dynamodb = self.session.resource('dynamodb', region_name='us-east-1')
        my_table = [ db for db in self.dynamodb_client.list_tables()['TableNames'] if db == table_name ]
        if my_table == []:
            self.create(table_name)
        self.table = self.dynamodb.Table(table_name)
        print(self.table)

    def create(self, table_name):
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
        print(self.table.scan()['Items'])

    def post_data(self, full_name, nickname, first_name, last_name, pathfinders_group, location):
        self.table.put_item(
            Item={
                'full_name':full_name,
                'nickname':nickname,
                'first_name':first_name,
                'last_name':last_name,
                'pathfinders_group':pathfinders_group,
                'location': location
            })

    #https://stackoverflow.com/questions/63497448/dynamodb-update-multiple-values
    def put_data(self, full_name, data):
        self.table.update_item(
            Key={'full_name':full_name},
            UpdateExpression= f'SET #KEY = :value',
            ExpressionAttributeNames={f'#KEY':key for key in data},
            ExpressionAttributeValues={f':value':data[key] for key in data  }
        )
    
    def delete_data(self, full_name):
        self.table.delete_item(Key={'full_name':full_name})

hello = apiAWS('temp-AGC', 'API_Project')
hello.post_data('spencer_sahu', "duck", 'spencer', 'sahu', 'protozoic', 'Iowa City')
#hello.post_data('edwin_duggirala', "edlose", 'edwin', 'durggirala', 'protozoic', 'San Antonio')
hello.put_data('spencer_sahu', {'gender':'male'})
hello.info()