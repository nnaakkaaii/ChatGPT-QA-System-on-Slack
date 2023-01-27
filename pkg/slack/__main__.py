import os
import datetime

from dotenv import load_dotenv

from . import Client

load_dotenv()

client = Client(
    access_token=os.environ.get('SLACK_ACCESS_TOKEN'),
    )
res = client.read(
    channel_id=os.environ.get('SLACK_CHANNEL_ID'),
    oldest=datetime.datetime.now() - datetime.timedelta(days=1),
    )
print(res)
print(res[0].is_addressing(os.environ.get('SLACK_BOT_ID')))
print(res[0].cleaned_text())

client.send(res[0])
