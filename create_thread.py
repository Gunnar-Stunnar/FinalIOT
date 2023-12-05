from openai import OpenAI
from secret import API_KEY


client = OpenAI(
  api_key=API_KEY,
)

print(f"Thread ID {client.beta.threads.create()}")