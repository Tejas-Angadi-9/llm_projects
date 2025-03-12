# Imports
import requests
from bs4 import BeautifulSoup
import ollama

# Constants
OLLAMA_API= "http://localhost:11434/api/chat"
HEADERS={"Content-Type": "application/json"}
MODEL="llama3.2"

# Usually same content is present. Inside messages we will have dictionaries with role as user and system.
messages = [{
    "role": "user",
    "content": "Describe some of the business applications of Generative AI"
}]

payload = {
    "model": MODEL,
    "messages": messages,
    "stream": False
}

# response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
response = ollama.chat(model=MODEL, messages=messages)
print(response.json()["message"]["content"])