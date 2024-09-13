---
layout: post
title: A Web App for AI-Enhanced Jekyll Blog Posts
date: 2024-09-13T17:28:00.822Z
---
In this post, we outline a web app concept called OllamaJekyllPublisher, designed to work with a locally installed Ollama model and Netlify for static deployment. This app allows users to generate content locally, review it, and seamlessly push updates to their AI-enhanced Jekyll blog.

Concept Overview
The OllamaJekyllPublisher is a web-based tool that interfaces with your local Ollama AI installation to help generate content for your Jekyll blog. Here’s how the system is structured:

Local Setup
Jekyll Blog: The blog is enhanced with AI features to make content generation smoother and more efficient.
Ollama Installation: Ollama runs locally to generate AI content.
Python Script: A Python script interfaces with Ollama, generating AI-driven content based on prompts.
Web App Features
1. Content Generation Interface
A simple web interface allows users to input blog details such as the title, tags, and initial content. Once submitted, AI-generated content like comments, FAQs, and summaries are created.

2. Ollama Integration
The Python backend sends requests from the web interface to the local Ollama installation, which generates the AI-driven content.

3. Content Preview and Editing
Users can review the generated content and edit it before publishing.

4. Git Integration
The app automatically commits changes to the local Git repository and pushes updates to the remote repository, triggering a Netlify deployment.

5. Netlify Deploy Status
A real-time status of the Netlify deployment is shown to the user.

Implementation Steps
Step 1: Create the Local Web Interface
This HTML/CSS/JavaScript frontend provides a simple interface for users to generate, preview, and publish AI-enhanced blog content.

html
Copy code
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OllamaJekyllPublisher</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>OllamaJekyllPublisher</h1>
    <form id="postForm">
        <input type="text" id="title" placeholder="Post Title" required>
        <input type="text" id="tags" placeholder="Tags (comma-separated)">
        <textarea id="content" placeholder="Initial Content" required></textarea>
        <button type="submit">Generate AI Content</button>
    </form>
    <div id="aiContent" style="display:none;">
        <h2>AI-Generated Content</h2>
        <div id="aiComments"></div>
        <div id="aiFAQ"></div>
        <div id="aiSummary"></div>
        <button id="publishButton">Publish Post</button>
    </div>
    <div id="deployStatus"></div>
    <script src="app.js"></script>
</body>
</html>
css
Copy code
/* style.css */
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

form {
    display: flex;
    flex-direction: column;
}

input, textarea, button {
    margin-bottom: 10px;
    padding: 5px;
}

button {
    cursor: pointer;
}

#aiContent {
    margin-top: 20px;
    border: 1px solid #ccc;
    padding: 10px;
}
javascript
Copy code
// app.js
document.getElementById('postForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const tags = document.getElementById('tags').value;
    const content = document.getElementById('content').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, tags, content })
    });

    const aiContent = await response.json();
    document.getElementById('aiComments').innerHTML = aiContent.comments;
    document.getElementById('aiFAQ').innerHTML = aiContent.faq;
    document.getElementById('aiSummary').innerHTML = aiContent.summary;
    document.getElementById('aiContent').style.display = 'block';
});
Step 2: Create the Python Backend
The backend interfaces with the local Ollama installation and manages Git operations.

python
Copy code
# app.py
from flask import Flask, request, jsonify
import subprocess
import git
from netlify_deploy_status import check_netlify_status

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    data = request.json
    title = data['title']
    tags = data['tags']
    content = data['content']

    comments = generate_ollama_content(f"Generate comments for: {title}\n{content}")
    faq = generate_ollama_content(f"Generate FAQ for: {title}\n{content}")
    summary = generate_ollama_content(f"Summarize: {title}\n{content}")

    return jsonify({
        'comments': comments,
        'faq': faq,
        'summary': summary
    })

@app.route('/publish', methods=['POST'])
def publish_post():
    repo = git.Repo('.')
    repo.git.add('.')
    repo.git.commit('-m', 'New blog post')
    repo.git.push()

    return jsonify({'success': True})

@app.route('/deploy-status')
def deploy_status():
    return jsonify(check_netlify_status())

def generate_ollama_content(prompt):
    result = subprocess.run(['ollama', 'run', 'mistral', prompt], capture_output=True, text=True)
    return result.stdout
Step 3: Check Netlify Deploy Status
python
Copy code
# netlify_deploy_status.py
import requests
import os

def check_netlify_status():
    site_id = os.getenv('NETLIFY_SITE_ID')
    token = os.getenv('NETLIFY_ACCESS_TOKEN')

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api.netlify.com/api/v1/sites/{site_id}/deploys', headers=headers)

    latest_deploy = response.json()[0]
    if latest_deploy['state'] == 'ready':
        return {'deployed': True}
    elif latest_deploy['state'] == 'error':
        return {'error': 'Deploy failed'}
    return {'deployed': False}
Step 4: Jekyll Layout for AI-Enhanced Posts
html
Copy code
<!-- _layouts/ai_enhanced_post.html -->
---
layout: post
---
{{ content }}

{% if page.ai_comments %}
<h2>AI-Generated Comments</h2>
{{ page.ai_comments | markdownify }}
{% endif %}

{% if page.ai_faq %}
<h2>AI-Generated FAQs</h2>
{{ page.ai_faq | markdownify }}
{% endif %}

{% if page.ai_summary %}
<h2>AI-Generated Summary</h2>
{{ page.ai_summary | markdownify }}
{% endif %}
Final Thoughts
This setup enables you to easily create, edit, and publish AI-enhanced blog posts to your Jekyll site, which can be automatically deployed through Netlify. It leverages local AI models (Ollama) while maintaining the simplicity of a static Jekyll site.

For further reading:

Explore Flask documentation to expand on the backend capabilities.
Read up on Jekyll’s official docs for advanced static site features.
Check out research papers on AI content generation to stay updated with the latest advancements.
Feel free to experiment with different models or modify the prompts to suit your content creation needs!