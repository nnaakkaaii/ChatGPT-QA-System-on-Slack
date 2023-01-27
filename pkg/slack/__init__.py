import dataclasses
import datetime
import re
from typing import Optional, List

from slack_sdk import WebClient


@dataclasses.dataclass(frozen=False)
class Message:
    channel_id: str
    text: str
    user: str
    ts: str
    
    ADDRESSER = '<@%s>'
    
    def is_addressing(self,
                      to: str) -> bool:
        return self.ADDRESSER % to in self.text
    
    def cleaned_text(self) -> str:
        r = re.sub(self.ADDRESSER % '.*',
                   '',
                   self.text,
                   )
        r = r.strip()
        return r
    
    @classmethod
    def from_response(cls,
                      channel_id: str,
                      response) -> Optional['Message']:
        if 'type' not in response:
            return None
        if 'blocks' not in response:
            return None
        if 'text' not in response:
            return None
        if 'user' not in response:
            return None
        if 'ts' not in response:
            return None
        return cls(
            channel_id=channel_id,
            text=response['text'],
            user=response['user'],
            ts=response['ts'],
            )
    
    def to_request(self):
        return {
            'channel': self.channel_id,
            'text': self.text,
            'thread_ts': self.ts,
            }


class Client:
    def __init__(self,
                 access_token: str,
                 ) -> None:
        self.client = WebClient(access_token)
    
    def read(self,
             channel_id: str,
             oldest: datetime.datetime,
             ) -> List[Message]:
        response = self.client.conversations_history(
            channel=channel_id,
            oldest=f'{oldest.timestamp():.6f}',
            )
        ret: List[Message] = []
        for r in response['messages']:
            m = Message.from_response(
                channel_id=channel_id,
                response=r,
                )
            if m is None:
                continue
            ret.append(m)
        return ret
    
    def send(self,
             msg: Message,
             ) -> None:
        self.client.chat_postMessage(**msg.to_request())
        return
