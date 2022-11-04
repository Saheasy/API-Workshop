import requests

data_spencer = {
                "first_name": "Spencer",
                "last_name": "Sahu",
                "nickname": "Duck",
                "pathfinders_group": "Protozoic",
                "location":"Iowa City"
            }

data_edwin = {
                "first_name": "Edwin",
                "last_name": "Duggirala",
                "nickname": "Edlose",
                "pathfinders_group": "Protozoic",
                "location":"San Antonio"
            }

url = "https://ubscztukk6.execute-api.us-east-1.amazonaws.com/dev/"

#print(requests.delete(url + "spencer_sahu" ).json())
#print(requests.post(url + "spencer_sahu", data=data_spencer ).json())
#print(requests.put(url + "spencer_sahu", data={"nickname": "Duckeasy"} ).json())
print(requests.get(url + "spencer_sahu" ).json())