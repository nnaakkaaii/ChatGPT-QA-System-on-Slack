import datetime
import os
import dataclasses

from pkg.chatgpt import Client as ChatGPTClient
from pkg.slack import Client as SlackClient


@dataclasses.dataclass(frozen=True)
class Config:
    slack_access_token: str
    slack_channel_id: str
    slack_bot_id: str
    chatgpt_conf_path: str
    min_interval: int
    
    @classmethod
    def from_env(cls) -> 'Config':
        return cls(
            slack_access_token=os.environ.get('SLACK_ACCESS_TOKEN'),
            slack_channel_id=os.environ.get('SLACK_CHANNEL_ID'),
            slack_bot_id=os.environ.get('SLACK_BOT_ID'),
            chatgpt_conf_path=os.environ.get('CHATGPT_CONF_PATH'),
            min_interval=int(os.environ.get('MIN_INTERVAL')),
            )
    
    def get_oldest(self) -> datetime.datetime:
        now = datetime.datetime.now()
        interval = datetime.timedelta(minutes=self.min_interval)
        return now - interval


def run(conf: Config):
    slack_client = SlackClient(conf.slack_access_token)
    messages = slack_client.read(conf.slack_channel_id,
                                 conf.get_oldest())

    chatgpt_client = None

    for m in messages:
        if not m.is_addressing(conf.slack_bot_id):
            continue

        text = m.cleaned_text()
        if text == '':
            continue

        if chatgpt_client is None:
            chatgpt_client = ChatGPTClient(conf.chatgpt_conf_path)

        m.text = chatgpt_client.ask(text)
        slack_client.send(m)


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    c = Config.from_env()
    run(c)
