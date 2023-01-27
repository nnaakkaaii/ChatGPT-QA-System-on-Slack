import json

from revChatGPT.ChatGPT import Chatbot


class Client:
    def __init__(self,
                 conf_path: str,
                 ) -> None:
        try:
            self.chatbot = Chatbot(json.load(open(conf_path, 'r')))
        except:
            self.chatbot = None

    def ask(self,
            text: str,
            ) -> str:
        try:
            r = self.chatbot.ask(text)
            return r['message']
        except:
            return 'ChatGPTの調子がわるいみたい...'
