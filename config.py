import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
GIGACHAT_TOKEN = os.getenv('GIGACHAT_TOKEN')

# noinspection PyBroadException
try:
    ADMIN_IDS = {int(admin_id) for admin_id in os.getenv('ADMIN_ID').split(",")}
except Exception:
    ADMIN_IDS = set()
