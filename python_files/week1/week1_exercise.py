import ollama

MODEL = "llama3.2"

english_text = """
Hello, how are you? I hope you're having a great day!
"""

translate_to = "Russian"

system_prompt = f"You are helpful translating tool which translates given English text to the specified language."
user_prompt = f"Translate the following English text  to {translate_to} language in just one line: \n\n{english_text}"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

response = ollama.chat(model=MODEL, messages=messages)
reply = response["message"]["content"]
print(reply)