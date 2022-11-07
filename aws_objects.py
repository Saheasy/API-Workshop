#Import the AWS SDK for Python
import boto3

#This is class with all of the AWS oriented code
class apiAWS:
    def __init__(self, profile_name, table_name):
        # Create a Session with the profile that has our A Cloud Guru Credentials
        self.session = boto3.Session(profile_name=profile_name)

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

    def post_data(self, full_name, nickname, first_name, last_name, pathfinders_group, location):
        # This is the equilivant of a post request, as it overwrites everything that's assigned to the 'full_name'
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
    
    def get_data(self, full_name):
        return self.table.get_item(Key={'full_name':full_name} )['Item']

    def delete_data(self, full_name):
        self.table.delete_item(Key={'full_name':full_name})

    def delete_table(self): 
        self.table.delete()

if __name__ == '__main__':
    hello = apiAWS('temp-AGC', 'API_Project')
    hello.post_data('spencer_sahu', "duck", 'spencer', 'sahu', 'protozoic', 'Iowa City')
    #hello.post_data('edwin_duggirala', "edlose", 'edwin', 'durggirala', 'protozoic', 'San Antonio')
    hello.put_data('spencer_sahu', 'gender', 'male')
    hello.put_data('spencer_sahu', 'nickname', 'Spence')
    hello.info()