import json


class Config:
    def __init__(self) -> None:
        with open("./settings.json") as file:
            self.settings=json.load(file)


    def get_value(self,key:str)->str:
        key_path=key.split('-')
        ans=self.settings
        for key in key_path:
            ans=ans[key]
        return ans
    
    def get_form_recognizer(self)->dict:
        return self.get_value("FormRecognizer")
    
    def get_content_moderator(self)->dict:
        return self.get_value("ContentModerator")
    
    def get_content_safety(self)->dict:
        return self.get_value("ContentSafety")
    
    def get_loremaster(self)->dict:
        return self.get_value("LoreMaster")
    
    def get_ai_service(self)->dict:
        return self.get_value("AIService")
    
    def get_language(self)->dict:
        return self.get_value("Language")
    
    def get_speech(self)->dict:
        return self.get_value("Speech")
    
    def get_conversation(self)->dict:
        return self.get_value("Conversation")
    
    def get_open_ai(self)->dict:
        return self.get_value("OpenAI")
    



if __name__=="__main__":
    c=Config()
    key=c.get_value("FormRecognizer-Key")
    end_point=c.get_value("FormRecognizer-EndPoint")
    print(end_point)
    

