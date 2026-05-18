import os
from dotenv import load_dotenv

load_dotenv()
tg_token = os.getenv('TG_TOKEN')
openai_token = os.getenv('OPENAI_TOKEN')


