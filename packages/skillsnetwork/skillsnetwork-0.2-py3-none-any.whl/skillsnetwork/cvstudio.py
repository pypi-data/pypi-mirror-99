import os
import requests
import json

# The absolute path of the directoy for this file:
_ROOT = os.path.abspath(os.path.dirname(__file__))

class CVStudio(object):
    def __init__(self, token, base_url='vision.skills.network'):
        self.token = token
        self.base_url = base_url

    def report(self, start_datetime, end_datetime, accuracy=None):
        url = 'https://' + self.base_url + '/api/report'
        report = {
            'started': start_datetime.strftime("%Y-%m-%dT%H:%M:%S.000+00:00"),
            'completed': end_datetime.strftime("%Y-%m-%dT%H:%M:%S.000+00:00"),
        }

        if accuracy is not None:
            report['accuracy'] = accuracy
        
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        
        x = requests.post(url, headers=headers, data=json.dumps(report))

        return x
