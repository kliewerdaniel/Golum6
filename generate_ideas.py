import requests
import json

def generate_blog_ideas(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.1",
        "prompt": f"Generate 5 blog post ideas about: {prompt}",
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

topic = input("Enter a topic for blog post ideas: ")
ideas = generate_blog_ideas(topic)
print(ideas)