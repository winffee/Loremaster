import json

import cv2 as cv
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from config import Config


class ContentSafety:
    def __init__(self) -> None:
        config=Config()
        settings=config.get_content_safety()
        endpoint=settings['EndPoint']
        key=settings['Key']
        self.credential=AzureKeyCredential(key=key)
        self.client=ContentSafetyClient(endpoint=endpoint,credential=self.credential)

    def analyze_text(self,text:str):
        request=AnalyzeTextOptions(text=text)
        try:
            response = self.client.analyze_text(request)
            response_data={
                "violence_result":response.violence_result.severity,
                "self_harm_result":response.self_harm_result.severity,
                "hate_result":response.hate_result.severity,
                "sexual_result":response.sexual_result.severity
            }
            return response_data
        except HttpResponseError as e:
            print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise



if __name__=="__main__":
    text="this is a violent text"
    cf=ContentSafety()
    cf.analyze_text(text=text)




