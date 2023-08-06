import requests
import json

from powerx_energy_api import config

class UserAPI():

    def __init__(self):
        self.access_token=None

    def login(self,username,password):
        print(f"api {config.BASE_USER_API_URL}/customer/login")
        x = requests.post(f'{config.BASE_USER_API_URL}/customer/login',
json={"username":username,'password':password})
        tx= json.loads(x.text)
        self.access_token = tx['access_token']
        print(f"response {self.access_token}")

    def get_current_heat(self,username,password):
        self.login(username,password)
        customer_info = self.get_customer_info()
        print(f"got customer info")
        if customer_info['preferences']['selected_hub_id'] is None:
            return 'No hub found',401
        hub_id = customer_info['preferences']['selected_hub_id']    
        x = requests.get(f'{config.BASE_USER_API_URL}/device/{hub_id}/heat/all/current_statistics',
    headers={
        'authorization':'Bearer '+self.access_token
    })
        print(f"heat output {x.text}")
        return json.loads(x.text)    

    def get_current_water(self,username,password):
        self.login(username,password)
        customer_info = self.get_customer_info()
        print(f"got customer info")
        if customer_info['preferences']['selected_hub_id'] is None:
            return 'No hub found',401
        hub_id = customer_info['preferences']['selected_hub_id']  
        x = requests.get(f'{config.BASE_USER_API_URL}/device/{hub_id}/water/all/current_statistics',
    headers={
        'authorization':'Bearer '+self.access_token
    })
        return json.loads(x.text)    

    def get_customer_info(self):
        x = requests.get(f'{config.BASE_USER_API_URL}/customer',
    headers={
        'authorization':'Bearer '+self.access_token
    })
        return json.loads(x.text)    
   
if __name__ == "__main__":
    api = UserAPI()
    api.get_current_water('manuel@powerx.co','test123')