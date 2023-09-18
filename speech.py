
from urllib.parse import urlencode

import requests

from config import Config


class Speech:
    def __init__(self) -> None:
        config=Config()
        settings=config.get_speech();
        self.endpoint=settings['EndPoint']
        self.key=settings['Key']
        

    def get_token(self)->str:
        headers = {
            # Request headers
            'Content-Type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': self.key,
        }
        try:
            response=requests.post(url=self.endpoint,json=None,headers=headers)
            return response.text
            #{'OriginalText': '"Is this a crap emai... WA 98052"', 'NormalizedText': '"   crap email abcde... WA 98052"', 'AutoCorrectedText': '"Is this a crap emai... WA 98052"', 'Misrepresentation': None, 'PII': {'Email': [...], 'IPA': [...], 'Phone': [...], 'Address': [...], 'SSN': [...]}, 'Classification': {'ReviewRecommended': True, 'Category1': {...}, 'Category2': {...}, 'Category3': {...}}, 'Language': 'eng', 'Terms': [{...}], 'Status': {'Code': 3000, 'Description': 'OK', 'Exception': None}, 'TrackingId': 'f227507a-fb76-4829-b...c74536189d'}
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


if __name__=="__main__":
    speech=Speech()
    token=speech.get_token()