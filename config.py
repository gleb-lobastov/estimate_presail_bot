import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
GIGACHAT_TOKEN = os.getenv('GIGACHAT_TOKEN')

# noinspection PyBroadException
try:
    ADMIN_ID = int(os.getenv('ADMIN_ID'))
except Exception:
    ADMIN_ID = 0
