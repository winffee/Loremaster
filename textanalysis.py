import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from config import Config


class TextAnalytics:
    def __init__(self) -> None:
        config = Config()
        settings = config.get_language()
        self.endpoint = settings['EndPoint']
        self.key = settings['Key']
        self.credential = AzureKeyCredential(self.key)
        self.client = TextAnalyticsClient(self.endpoint, self.credential)
        self.projectname = 'loremaster'
        self.deploymentname = 'loremaster'

    def analyze_text(self, text: str):
        document=[text]
        poller=self.client.begin_extract_summary(documents=document)
        #poller = self.client.begin_abstract_summary(document)
        results=poller.result()
        final_result=''
        for result in results:
            if result.kind=="AbstractiveSummarization":
                final_result=result.summaries[0].text
            if result.kind=="ExtractiveSummarization":
                for s in result.sentences:
                    final_result+="\n"+s.text
            elif result.kind=="DocumentError":
                final_result="Code:{0}. Message:{1}".format(result.error.code,result.error.message)
        return final_result


if __name__ == "__main__":
    textAnalyzer = TextAnalytics()
    documents = [
        """I had the best day of my life. I decided to go sky-diving and it made me appreciate my whole life so much more.
    I developed a deep-connection with my instructor as well, and I feel as if I've made a life-long friend in her.""",
        """This was a waste of my time. All of the views on this drop are extremely boring, all I saw was grass. 0/10 would
    not recommend to any divers, even first timers.""",
        """This was pretty good! The sights were ok, and I had fun with my instructors! Can't complain too much about my experience""",
        """I only have one word for my experience: WOW!!! I can't believe I have had such a wonderful skydiving company right
    in my backyard this whole time! I will definitely be a repeat customer, and I want to take my grandmother skydiving too,
    I know she'll love it!"""
    ]
    poller=textAnalyzer.analyze_text(documents)
    abstractive_summary_results = poller.result()
    for result in abstractive_summary_results:
        if result.kind == "AbstractiveSummarization":
            print("Summaries abstracted:")
            [print(f"{summary.text}\n") for summary in result.summaries]
    abc=123
