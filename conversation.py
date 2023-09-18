from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.credentials import AzureKeyCredential

from config import Config


class ConversationUnderstanding:
    def __init__(self) -> None:
        config=Config()
        settings=config.get_conversation()
        self.endpoint=settings['EndPoint']
        self.key=settings['Key']
        self.credential=AzureKeyCredential(self.key)
        self.client=ConversationAnalysisClient(self.endpoint,self.credential)
        self.projectname='loremaster'
        self.deploymentname='loremaster'

    
    def analyze_query(self,query:str):
        task={
                    "kind":"Conversation",
                    "analysisInput":{
                        "conversationItem":{
                            "participantId":"1",
                            "id":"1",
                            "modality":"text",
                            "language":"en",
                            "text":query
                        },
                        "isLoggingEnabled":False
                    },
                    "parameters":{
                        "projectName":self.projectname,
                        "deploymentName":self.deploymentname,
                        "verbose":True,
                        "stringIndexType":"TextElement_V8"
                    }
             }
        with self.client:
            result=self.client.analyze_conversation(task=task)
            return result


if __name__=="__main__":
    c=ConversationUnderstanding()
    query="take her picture"
    res=c.analyze_query(query=query)
    abc=123
