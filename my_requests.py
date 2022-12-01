import requests

data_spencer = {
                "nickname": "Duck",
                "group": "Protozoic",
                "location":"Iowa City"
            }

data_edwin = {
                "nickname": "Edlose",
                "pathfinders_group": "Protozoic",
                "location":"San Antonio"
            }

url = "http://127.0.0.1:5000/aws"
headers = {"Content-Type": "application/json"}
#print(requests.delete(url + "spencer_sahu" ).json())
print(requests.post(url + "spencer_sahu", data=data_spencer, headers=headers ))
#print(requests.put(url + "spencer_sahu", data={"nickname": "Duckeasy"} ).json())
print(requests.get(url).json())