import cv2 as cv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from config import Config


class FormRecognizer:
    def __init__(self) -> None:
        config=Config()
        settings=config.get_form_recognizer()
        self.endpoint=settings['EndPoint']
        self.credential=AzureKeyCredential(settings['Key'])
        self.client=DocumentAnalysisClient(endpoint=self.endpoint,credential=self.credential)

    def get_text(self,document_bytes:bytes)->str:
        result=self.client.begin_analyze_document('prebuilt-read',document=document_bytes)
        paragraphs=result.result().to_dict()['paragraphs']
        text=''
        for para in paragraphs:
            text+=para['content']
        return text





if __name__=="__main__":
    fr=FormRecognizer()
    path='./static/captured_image.jpg'
    image=cv.imread(path)
    if image is not None:
        byte_arr=cv.imencode('.jpg',image)[1].tobytes()
        ans=fr.get_text(byte_arr)
    
    print(ans)
    
