from dotenv import load_dotenv

from . import Client

load_dotenv()

client = Client('./conf/config.json')
print(client.ask('あなたについて教えてください。'))
