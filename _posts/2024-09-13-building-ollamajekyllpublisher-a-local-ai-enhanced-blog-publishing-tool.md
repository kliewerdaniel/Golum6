---
layout: post
title: "Building OllamaJekyllPublisher: A Local AI-Enhanced Blog Publishing Tool"
date: 2024-09-13T17:52:20.952Z
---
In this post, I'll outline a web app concept designed to work with a locally run Ollama installation and Netlify for static deployment. This app, which we'll call "OllamaJekyllPublisher," will allow users to generate content locally and easily push updates to their AI-enhanced Jekyll blog.

## Introducing OllamaJekyllPublisher

The concept of this app is simple: a local web interface that lets you generate AI-enhanced blog posts using your local Ollama setup, and automatically push the generated content to a Jekyll blog hosted on Netlify.

### Local Setup Requirements:

1. A Jekyll blog with AI-enhancement features already set up
2. Ollama installed locally
3. A Python script to interface with Ollama and generate content

## Web App Features

### a. Content Generation Interface

- A simple web interface (HTML, CSS, JavaScript) that runs locally
- Forms for inputting blog post details (title, tags, initial content)
- Buttons to trigger AI-enhanced content generation (comments, FAQs, summaries, etc.)

### b. Ollama Integration

- Use the local Ollama installation to generate content
- Python backend to handle requests from the web interface to Ollama

### c. Preview and Edit

- Display generated content for user review
- Allow users to edit or regenerate AI content before publishing

### d. Git Integration

- Automatically commit changes to the local Git repository
- Push changes to the remote repository (which triggers Netlify deployment)

### e. Netlify Deploy Status

- Show the status of the Netlify deployment

## Implementation Steps

### Step 1: Create the Local Web Interface

Let's start by creating the HTML, CSS, and JavaScript files for our local web interface.

#### `index.html`

```html
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
```

#### `style.css`

```css
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
```

#### `app.js`

```javascript
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

document.getElementById('publishButton').addEventListener('click', async () => {
    const response = await fetch('/publish', { method: 'POST' });
    const result = await response.json();
    if (result.success) {
        alert('Post published and pushed to GitHub!');
        checkDeployStatus();
    } else {
        alert('Error publishing post: ' + result.error);
    }
});

async function checkDeployStatus() {
    const statusElement = document.getElementById('deployStatus');
    statusElement.innerHTML = 'Checking deploy status...';

    const checkStatus = async () => {
        const response = await fetch('/deploy-status');
        const status = await response.json();
        if (status.deployed) {
            statusElement.innerHTML = 'Deploy successful!';
        } else if (status.error) {
            statusElement.innerHTML = 'Deploy failed: ' + status.error;
        } else {
            statusElement.innerHTML = 'Deploying...';
            setTimeout(checkStatus, 5000);
        }
    };

    checkStatus();
}
```

### Step 2: Create the Python Backend

Now, let's create the Python backend that will handle requests from our web interface and interact with Ollama and Git.

#### `app.py`

```python
from flask import Flask, request, jsonify
import subprocess
import os
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

    comments = generate_ollama_content(f"Generate comments for blog post: {title}\n{content}")
    faq = generate_ollama_content(f"Generate FAQ for blog post: {title}\n{content}")
    summary = generate_ollama_content(f"Summarize blog post: {title}\n{content}")

    return jsonify({
        'comments': comments,
        'faq': faq,
        'summary': summary
    })

@app.route('/publish', methods=['POST'])
def publish_post():
    try:
        create_post_file()

        repo = git.Repo('.')
        repo.git.add('.')
        repo.git.commit('-m', 'Add new blog post')
        repo.git.push()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/deploy-status')
def deploy_status():
    return jsonify(check_netlify_status())

def generate_ollama_content(prompt):
    result = subprocess.run(['ollama', 'run', 'mistral', prompt], capture_output=True, text=True)
    return result.stdout

def create_post_file():
    # Implementation for creating the Jekyll post file
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

### Step 3: Checking Netlify Deploy Status

Finally, let's create a script to check the status of Netlify deployment:

#### `netlify_deploy_status.py`

```python
import requests
import os

def check_netlify_status():
    site_id = os.environ.get('NETLIFY_SITE_ID')
    token = os.environ.get('NETLIFY_ACCESS_TOKEN')

if not site_id or not token:
        return {'error': 'Netlify credentials not set'}

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api.netlify.com/api/v1/sites/{site_id}/deploys', headers=headers)

    if response.status_code != 200:
        return {'error': 'Failed to fetch deploy status'}

    deploys = response.json()
    if not deploys:
        return {'error': 'No deploys found'}

    latest_deploy = deploys[0]
    if latest_deploy['state'] == 'ready':
        return {'deployed': True}
    elif latest_deploy['state'] == 'error':
        return {'error': 'Deploy failed'}
    else:
        return {'deployed': False}
```

## Conclusion

With this setup, users can now easily create AI-enhanced blog posts and update their Jekyll site hosted on Netlify, all from a local web interface. This system combines the power of local AI generation with static site deployment, streamlining the process of publishing high-quality, AI-enhanced content.

The OllamaJekyllPublisher tool we've created offers several key benefits:

1. **Local AI Processing**: By using Ollama locally, we maintain control over our AI processing and avoid potential privacy concerns associated with cloud-based AI services.

2. **Customizable Content Generation**: The tool allows for easy customization of AI-generated content, including comments, FAQs, and summaries.

3. **Seamless Integration**: The integration with Git and Netlify automates the process of publishing and deploying updates to the blog.

4. **User-Friendly Interface**: The simple web interface makes it easy for users to generate and publish content without needing to interact directly with the command line or Git.

5. **Real-time Deployment Status**: Users can see the status of their Netlify deployment right in the interface, providing immediate feedback on the publishing process.

## Next Steps

While this tool provides a solid foundation for AI-enhanced blog publishing, there are several ways it could be expanded and improved:

1. **Multiple AI Models**: Implement support for different Ollama models, allowing users to choose the best model for their specific content needs.

2. **Content Versioning**: Add the ability to save and load different versions of AI-generated content before publishing.

3. **Enhanced Editing**: Implement a rich text editor for more advanced content editing capabilities.

4. **SEO Optimization**: Integrate AI-powered SEO suggestions to help optimize blog posts for search engines.

5. **Image Generation**: Add support for AI image generation to complement blog posts.

6. **Analytics Integration**: Incorporate blog analytics to provide insights on post performance directly in the tool.

By building and using tools like OllamaJekyllPublisher, we can harness the power of AI to enhance our content creation process while maintaining control over our data and publishing workflow. This approach allows us to create more engaging, informative blog posts with less effort, freeing up time to focus on the core ideas and messages we want to share with our audience.

Remember, the key to successful AI-enhanced blogging is to use these tools as aids to augment and inspire your writing, not to replace your unique voice and perspective. Happy blogging!