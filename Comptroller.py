'''
Initial Draft for Comptrollers Checkbook

-- Needs to be checked -- Information being returned is invalid

'''

import requests

class Checkbook:
    def __init__(self,ID,Key):
        '''
        (Create Comptroller Object)
        (Ex) Object = Comptroller.Checkbook('API ID','API Key')
        '''
        self.id = ID
        self.key = Key
        
        #Constants
        self.headers = {'app_id': self.id,'app_key' : self.key }
        self.url = 'https://api.cityofnewyork.us/comptroller/v1/api'
    def callCheckbook(self):
        self.r = requests.post(self.url, data=self.headers , headers=self.headers)
        print self.r.status_code
        print self.r.text
