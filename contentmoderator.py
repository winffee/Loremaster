import base64
import json
from urllib.parse import urlencode

import requests

from config import Config


class ContentModerator:
    def __init__(self) -> None:
        config=Config()
        settings=config.get_content_moderator()
        self.endpoint=settings['EndPoint']
        self.key=settings['Key']

    def call_api(self,data:str):
        headers = {
            # Request headers
            'Content-Type': 'text/plain',
            'Ocp-Apim-Subscription-Key': self.key,
        }
        params = urlencode({
            # Request parameters
            'autocorrect': 'True',
            'PII': 'True',
            'listId': '',
            'classify': 'True',
            'language': 'eng',
        })
        url=self.endpoint+"/contentmoderator/moderate/v1.0/ProcessText/Screen?{params}".format(params=params)
        try:
            data=data
            response=requests.post(url,data=data,headers=headers)
            response_data=json.loads(response.content)
            return response_data
            #{'OriginalText': '"Is this a crap emai... WA 98052"', 'NormalizedText': '"   crap email abcde... WA 98052"', 'AutoCorrectedText': '"Is this a crap emai... WA 98052"', 'Misrepresentation': None, 'PII': {'Email': [...], 'IPA': [...], 'Phone': [...], 'Address': [...], 'SSN': [...]}, 'Classification': {'ReviewRecommended': True, 'Category1': {...}, 'Category2': {...}, 'Category3': {...}}, 'Language': 'eng', 'Terms': [{...}], 'Status': {'Code': 3000, 'Description': 'OK', 'Exception': None}, 'TrackingId': 'f227507a-fb76-4829-b...c74536189d'}
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__=="__main__":
    cm=ContentModerator()
    cm.call_api("abc")
