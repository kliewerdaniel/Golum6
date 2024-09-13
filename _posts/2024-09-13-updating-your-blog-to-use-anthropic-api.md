---
layout: post
title: Updating Your Jekyll Blog to Use Anthropic API
date: 2024-09-13T11:51:00.000Z
---
# Updating Your Jekyll Blog to Use Anthropic API
## 1. Install Required Python Packages
First, make sure you have the necessary Python packages installed:
pip install anthropic requests
## 2. Update the AI Content Generator Script
Replace the contents of `ai_content_generator.py` with the following:
import sys
import anthropic
import os
# Set your Anthropic API key as an environment variable
os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"
client = anthropic.Client()
def generate_ai_content(prompt):
response = client.completion(
prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
model="claude-2",
max_tokens_to_sample=300,
)
return response.completion
def generate_blog_post(title):
prompt = f"Write a short blog post with the title: {title}"
return generate_ai_content(prompt)
def generate_comments(post_content):
prompt = f"Generate 3 short, diverse comments for the following blog post:\n\n{post_content}"
return generate_ai_content(prompt)
if __name__ == "__main__":
if len(sys.argv) < 2:
print("Usage: python ai_content_generator.py <title>")
sys.exit(1)
title = sys.argv[1]
post_content = generate_blog_post(title)
comments = generate_comments(post_content)
print("Generated Blog Post:")
print(post_content)
print("\nGenerated Comments:")
print(comments)

## 3. Secure Your API Key
Instead of hardcoding your API key, it's best to use environment variables. You can set this in your shell:

export ANTHROPIC_API_KEY="your_actual_api_key_here"

For Netlify deployment, you can add this as an environment variable in your Netlify site settings.
## 4. Update the Jekyll Plugin
The Jekyll plugin (`_plugins/ai_content_generator.rb`) doesn't need to change, as it still calls the Python script in the same way.
## 5. Test Locally
Run your Jekyll site locally to test the changes:

bundle exec jekyll serve

## 6. Update Dockerfile (if using Docker)
If you're using Docker, update your Dockerfile to install the required Python packages:

# ... (existing Dockerfile content)
# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip
# Install required Python packages
RUN pip3 install anthropic requests
# ... (rest of your Dockerfile)

## 7. Update docker-compose.yml
If you're using Docker Compose, update your `docker-compose.yml` to pass the API key as an environment variable:

version: '3'
services:
site:
# ... (existing configuration)
environment:
- ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

## 8. Deploy to Netlify
Push your changes to GitHub, and Netlify will automatically deploy your updated site.
Remember to add the `ANTHROPIC_API_KEY` as an environment variable in your Netlify site settings.
## 9. Create a New Blog Post to Test
Create a new blog post using Netlify CMS or manually in the `_posts` directory to test the AI-enhanced features.
## 10. Fine-tune and Iterate
Experiment with different prompts and settings in the `ai_content_generator.py` script to get the best results for your blog.
---
That's it! Your Jekyll blog is now updated to use the Anthropic API for AI-enhanced content generation. The key changes are in the `ai_content_generator.py` script, where we've replaced the Ollama-specific code with Anthropic API calls. 
