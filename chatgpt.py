import openai

from config import Config


class ChatGPT:
    def __init__(self) -> None:
        config = Config()
        settings = config.get_open_ai()
        self.api_type = "azure"
        self.api_base = settings["EndPoint"]
        self.api_key = settings["Key"]
        openai.api_key=self.api_key
        openai.api_base=self.api_base
        openai.api_type="azure"
        openai.api_version="2023-05-15"
        self.api_version = "2023-05-15"

    def get_response(self, data:list)->str:
        response = openai.ChatCompletion.create(
            engine="loremaster-gpt-35-turbo",
            messages=data
        )
        return response['choices'][0]['message']['content']


if __name__=="__main__":
    chatgpt=ChatGPT()
    chatgpt.get_response("How can I learn python?")
    abc=123
