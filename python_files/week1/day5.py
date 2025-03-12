# Imports
import os
import requests
from bs4 import BeautifulSoup
import ollama
import json

# Defining model
MODEL = "llama3.2"

# Header
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

# Creating a website class
class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No Title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
                self.text = soup.body.get_text(separator='\n', strip=True)
        else:
            self.text = ""

        links = [link.get('href') for link in soup.find_all('a')]
        self.links = links

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    
ed = Website("https://edwarddonner.com")
# print(ed.links)

#* To call the llama 3.2, we have to do some configuration, so we can get the correct data as we expect
link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://full.url/goes/here/careers"}
    ]
}
"""

# print(link_system_prompt)

#* Build the user prompt
def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

# print(get_links_user_prompt(ed))

#* Call the llama3.2 model
def get_links(url):
    website = Website(url)
    messages = [
        {"role": "system", "content": link_system_prompt},
        {"role": "user", "content": get_links_user_prompt(website)}
    ]
    response = ollama.chat(model=MODEL, messages=messages)
    return response["message"]["content"]

# huggingface = Website("https://huggingface.co")
# print(huggingface.links)
# print(get_links("https://huggingface.co"))

def get_all_details(url):
    result = "Landing Page:\n"
    result += Website(url).get_contents()

    links = get_links(url)
    if not links:
        print("Links not found or generated properly!")
        return
    
    try:
        links_dict = json.loads(links)  # Ensure it's valid JSON
    except json.JSONDecodeError:
        print("Error: The response from the model is not valid JSON.")
        return
    
    for link in links_dict.get("links", []):
        print(link)

get_all_details("https://huggingface.co")
# print(get_all_details("https://huggingface.co"))