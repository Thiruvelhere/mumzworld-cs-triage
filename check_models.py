import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url='https://openrouter.ai/api/v1', api_key=os.environ['OPENROUTER_API_KEY'])
models = client.models.list()
free = [m.id for m in models.data if ':free' in m.id]
print('\n'.join(free))