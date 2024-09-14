---
layout: home
title: "Creating an AI-Enhanced Jekyll Blog: From Setup to LLM Integration"
date: 2024-09-14T12:46:46.145Z
---
Introduction:

In this comprehensive guide, I'll walk you through the process of creating a Jekyll blog with Netlify CMS, Docker integration, and how to enhance it with locally-hosted large language models (LLMs). We'll cover everything from initial setup to advanced AI integration, with tips on using GitHub Desktop and Netlify for seamless deployment.

Part 1: Setting Up Your Jekyll Blog

1.1 Initial Setup:
To begin, we'll use a shell script to automate much of the initial setup. Here's a breakdown of what our script (let's call it `setup_blog.sh`) does:

```bash
#!/bin/bash

# Create new Jekyll site
jekyll new my_awesome_blog
cd my_awesome_blog

# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create Dockerfile
echo "FROM jekyll/jekyll:4.2.0
WORKDIR /srv/jekyll
COPY . .
RUN bundle install
CMD [\"jekyll\", \"serve\", \"--force_polling\", \"-H\", \"0.0.0.0\"]" > Dockerfile

# Create docker-compose.yml
echo "version: '3'
services:
  site:
    command: jekyll serve --force_polling
    image: jekyll/jekyll:4.2.0
    volumes:
      - .:/srv/jekyll
    ports:
      - 4000:4000" > docker-compose.yml

# Set up Netlify CMS
mkdir -p admin
echo "backend:
  name: git-gateway
  branch: main
media_folder: \"assets/uploads\"
collections:
  - name: \"blog\"
    label: \"Blog\"
    folder: \"_posts\"
    create: true
    slug: \"{{year}}-{{month}}-{{day}}-{{slug}}\"
    fields:
      - {label: \"Layout\", name: \"layout\", widget: \"hidden\", default: \"post\"}
      - {label: \"Title\", name: \"title\", widget: \"string\"}
      - {label: \"Publish Date\", name: \"date\", widget: \"datetime\"}
      - {label: \"Body\", name: \"body\", widget: \"markdown\"}" > admin/config.yml

echo "<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Content Manager</title>
</head>
<body>
  <script src=\"https://unpkg.com/netlify-cms@^2.0.0/dist/netlify-cms.js\"></script>
</body>
</html>" > admin/index.html

# Build and run Docker container
docker-compose up -d
```

This script creates a new Jekyll site, sets up Git, creates necessary Docker files, and configures Netlify CMS.

1.2 Using GitHub Desktop:
After running the script, open GitHub Desktop and follow these steps:
1. Click "Add an Existing Repository from your Hard Drive"
2. Navigate to your blog's directory and select it
3. In the "Repository name" field, enter a name for your GitHub repository
4. Click "Create Repository"
5. Click "Publish repository" to push your local repository to GitHub

Tip: Use GitHub Desktop's "History" tab to review changes before committing. This helps in maintaining a clean commit history.

1.3 Deploying with Netlify:
1. Log in to your Netlify account
2. Click "New site from Git"
3. Choose GitHub as your Git provider
4. Select your blog repository
5. Set the build command to `jekyll build` and the publish directory to `_site/`
6. Click "Deploy site"

Tip: Enable "Deploy previews" in Netlify settings to review changes before they go live on your main site.

Part 2: Integrating Large Language Models

2.1 Setting Up OpenWebUI with Docker:
OpenWebUI is an open-source ChatG
PT-like interface that can work with various LLMs. Let's set it up using Docker:

1. Create a new directory for OpenWebUI:
   ```bash
   mkdir openwebui && cd openwebui
   ```

2. Create a `docker-compose.yml` file:
   ```yaml
   version: '3'
   services:
     openwebui:
       image: ghcr.io/open-webui/open-webui:main
       ports:
         - 8080:8080
       environment:
         - OLLAMA_API_BASE_URL=http://ollama:11434/api
       depends_on:
         - ollama
     ollama:
       image: ollama/ollama
       volumes:
         - ./ollama_data:/root/.ollama
   ```

3. Start the containers:
   ```bash
   docker-compose up -d
   ```

Now, you can access OpenWebUI at `http://localhost:8080`.

2.2 Using Free Models with OpenWebUI:
1. Open OpenWebUI in your browser
2. Click on "Model" in the top-right corner
3. Select "Download new model"
4. Choose a free model like "llama2" or "mistral"
5. Wait for the model to download and initialize

Tip: Smaller models like "tinyllama" or "orca-mini" are faster to download and run on less powerful hardware.

2.3 Integrating LLM-generated Content into Your Blog:
Now that we have a local LLM running, let's create a script to generate blog post ideas:

```python
import requests
import json

def generate_blog_ideas(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama2",
        "prompt": f"Generate 5 blog post ideas about: {prompt}",
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

topic = input("Enter a topic for blog post ideas: ")
ideas = generate_blog_ideas(topic)
print(ideas)
```

Save this as `generate_ideas.py` in your blog's root directory.

Part 3: Streamlining Your Workflow

3.1 Creating a Master Setup Script:
Let's create a master script that combines all our setup steps:

```bash
#!/bin/bash

# Run Jekyll setup
./setup_blog.sh

# Set up OpenWebUI
mkdir openwebui && cd openwebui
echo "version: '3'
services:
  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - 8080:8080
    environment:
      - OLLAMA_API_BASE_URL=http://ollama:11434/api
    depends_on:
      - ollama
  ollama:
    image: ollama/ollama
    volumes:
      - ./ollama_data:/root/.ollama" > docker-compose.yml
docker-compose up -d

cd ..

# Install Python dependencies
pip install requests

echo "Setup complete! Your blog is ready at http://localhost:4000"
echo "OpenWebUI is available at http://localhost:8080"
```

Save this as `master_setup.sh`.

3.2 GitHub Desktop Workflow Tips:
- Use branches for different features or posts
- Utilize the "Fetch origin" button regularly to stay updated with remote changes
- Take advantage of the diff view to review changes before committing

3.3 Netlify Deployment Tips:
- Set up branch deploys to preview changes from non-main branches
- Use deploy contexts to customize build settings for different branches
- Leverage Netlify Functions for serverless backend functionality

Conclusion:
We've covered setting up a Jekyll blog with Netlify CMS, integrating it with GitHub and Netlify for easy deployment, and enhancing it with locally-hosted LLMs using OpenWebUI. By leveraging shell scripts and Docker, we've created a streamlined workflow that combines the power of static site generators with the flexibility of AI-assisted content creation.

Remember to always respect licensing terms when using open-source modelsand be mindful of the computational resources required when running LLMs locally.

Part 4: Advanced LLM Integration Techniques

4.1 Automating Content Generation:
Let's expand our LLM integration by creating a script that generates entire blog post drafts:

```python
import requests
import json
import frontmatter
from datetime import datetime

def generate_blog_post(title):
    url = "http://localhost:11434/api/generate"
    prompt = f"""Write a blog post with the title: "{title}"
    Include the following sections:
    1. Introduction
    2. Main points (at least 3)
    3. Conclusion
    Make the content informative and engaging, around 500 words."""
    
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

def save_blog_post(title, content):
    post = frontmatter.Post(content)
    post['layout'] = 'post'
    post['title'] = title
    post['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    filename = f"_posts/{datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
    
    with open(filename, 'wb') as f:
        frontmatter.dump(post, f)
    
    print(f"Blog post saved as {filename}")

if __name__ == "__main__":
    title = input("Enter the blog post title: ")
    content = generate_blog_post(title)
    save_blog_post(title, content)
```

Save this as `generate_post.py`. This script generates a full blog post draft and saves it in the correct format for Jekyll.

4.2 Implementing AI-Powered Comments:
To simulate user engagement, we can create an AI-powered commenting system:

```python
import requests
import json
import random

def generate_comment(post_content):
    personas = [
        "Enthusiastic Beginner",
        "Skeptical Expert",
        "Curious Learner",
        "Devil's Advocate"
    ]
    persona = random.choice(personas)
    
    url = "http://localhost:11434/api/generate"
    prompt = f"""As a {persona}, write a comment on the following blog post:

    {post_content}

    Keep the comment under 100 words and stay in character."""
    
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

# Example usage
post_content = "Your blog post content here..."
comment = generate_comment(post_content)
print(comment)
```

Save this as `generate_comment.py`. You can integrate this with your blog's commenting system to add AI-generated comments for increased engagement.

4.3 Fine-tuning LLMs for Your Blog's Style:
To make the AI-generated content more aligned with your writing style, consider fine-tuning the model:

1. Prepare a dataset of your existing blog posts in a format suitable for fine-tuning (e.g., JSON Lines).
2. Use Ollama's fine-tuning capabilities or a tool like `lora-trainer` for efficient fine-tuning.
3. Create a new Ollama model with your fine-tuned weights.

This process will help the LLM generate content that more closely matches your unique voice and style.

Part 5: Optimizing Performance and Security

5.1 Caching LLM Responses:
To reduce load on your local machine and improve response times, implement a caching system:

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached_llm_request(prompt, model="llama2", expiration=3600):
    cache_key = f"{model}:{prompt}"
    cache
d_response = redis_client.get(cache_key)
    
    if cached_response:
        return json.loads(cached_response)
    
    # If not in cache, make the actual LLM request
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    result = json.loads(response.text)["response"]
    
    # Cache the result
    redis_client.setex(cache_key, expiration, json.dumps(result))
    
    return result

# Example usage
prompt = "What are the benefits of static site generators?"
response = cached_llm_request(prompt)
print(response)
```

This caching system uses Redis to store LLM responses, reducing redundant computations and speeding up repeated queries.

5.2 Implementing Rate Limiting:
To prevent overuse of your local LLM, implement a simple rate limiting mechanism:

```python
from functools import wraps
import time

def rate_limit(max_calls, time_frame):
    calls = []
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=5, time_frame=60)
def generate_blog_post(title):
    # Your existing generate_blog_post function here
    pass
```

This decorator limits the number of calls to the `generate_blog_post` function to 5 times per minute.

5.3 Securing Your Local LLM:
While running an LLM locally is generally more secure than using cloud-based services, it's still important to implement some basic security measures:

1. Use a firewall to restrict access to the Ollama API (port 11434) and OpenWebUI (port 8080) to only your local network.
2. Implement authentication for OpenWebUI by setting up a reverse proxy with basic auth.
3. Regularly update your Ollama and OpenWebUI installations to get the latest security patches.

Part 6: Enhancing Your Blog with AI-Powered Features

6.1 Automated Content Summarization:
Create a script to automatically generate summaries for your blog posts:

```python
def summarize_post(content):
    url = "http://localhost:11434/api/generate"
    prompt = f"""Summarize the following blog post in 3-4 sentences:

    {content}

    Provide a concise summary that captures the main points."""
    
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

# Add this to your post generation workflow
summary = summarize_post(post_content)
post['summary'] = summary  # Add to frontmatter
```

6.2 AI-Powered SEO Optimization:
Implement an AI assistant to help optimize your posts for search engines:

```python
def seo_optimize(title, content):
    url = "http://localhost:11434/api/generate"
    prompt = f"""Given the following blog post title and content, suggest 5 SEO improvements:

    Title: {title}
    Content: {content}

    Provide specific suggestions for:
    1. Title optimization
    2. Meta description
    3. Keyword density
    4. Header structure
    5. Internal linking"""
    
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

# Use this function after generating a blog post to get SEO suggestions
seo_suggestions = seo_optimize(post_title, post_content)
print(seo_suggestions)
```

6.3 Automated Content Scheduling:
Create a system to automatically generate and schedule blog posts:

```python
import schedule
import time
from generate_post import generate_blog_post, save_blog_post

def create_scheduled_post():
    topics = [
        "Latest trends in web development",
        "Improving blog performance",
        "AI integration in content creation",
        "Best practices for Jekyll blogs",
        "Leveraging Netlify for static sites"
    ]
    topic = random.choice(topics)
    title = f"Weekly Insights: {topic}"
    content = generate_blog_post(title)
    save_blog_post(title, content)
    print(f"Scheduled post created: {title}")

# Schedule a new post every Monday at 9 AM
schedule.every().monday.at("09:00").do(create_scheduled_post)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Run this script in the background to automatically generate and publish weekly blog posts.

Part 7: Advanced GitHub and Netlify Integration

7.1 GitHub Actions for Automated Testing:
Create a GitHub Action to automatically test your Jekyll site before deployment:

```yaml
name: Jekyll site CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Ruby
      uses: ruby/setup-ruby@v1
      with:
        ruby-version: 2.7
    - name: Install dependencies
      run: |
        gem install bundler
        bundle install
    - name: Build site
      run: bundle exec jekyll build
    - name: Run tests
      run: bundle exec htmlproofer ./_site --check-html --disable-external
```

This action builds your Jekyll site and runs HTMLProofer to check for broken links and HTML issues.

7.2 Netlify Build Plugins:
Enhance your Netlify builds with plugins. For example, to automatically optimize images:

1. Install the Netlify CLI: `npm install netlify-cli -g`
2. Add the following to your `netlify.toml` file:

```toml
[[plugins]]
package = "netlify-plugin-image-optim"

[plugins.inputs]
# Include SVG files
include_svg = true
# Ignore PNG files
ignore = ["*.png"]
```

This plugin will automatically optimize your images during the Netlify build process.

7.3 Custom Netlify Functions:
Create a Netlify Function to handle dynamic content, such as a contact form:

1. Create a `netlify/functions` directory in your project root.
2. Add a `contact-form.js` file:

```javascript
exports.handler = async (event, context) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const { name, email, message } = JSON.parse(event.body);

  // Here you would typically send an email or save to a database
  console.log(`Received message from ${name} (${email}): ${message}`);

  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Thank you for your message!" }),
  };
};
```

3. Update your `netlify.toml` to include:

```toml
[functions]
  directory = "netlify/functions"
```

Now you can use this function to handle form submissions without a backend server.

Conclusion:
We've covered a wide range of topics, from setting up a Jekyll blog with Netlify CMS to integrating AI-powered features using locally-hosted LLMs. We've also explored advanced GitHub and Netlify integrations to streamline your workflow and enhance your blog's functionality.

Remember that while AI can greatly assist in content creation and blog management, it's important to maintain your unique voice and ensure the quality of the content. Always review and edit AI-generated content before publishing to ensure it meets your standards and accurately represents your thoughts and expertise.

Here are some final tips and considerations:

1. Continuous Learning: Stay updated with the latest developments in Jekyll, Netlify, and AI technologies. The field is rapidly evolving, and new tools and techniques are constantly emerging.

2. Performance Monitoring: Regularly monitor your blog's performance using tools like Google PageSpeed Insights or Lighthouse. Optimize images, minify CSS and JavaScript, and leverage browser caching to ensure fast load times.

3. SEO Best Practices: While our AI-powered SEO tool can provide valuable suggestions, make sure to stay informed about current SEO best practices. Regularly update your content, use descriptive URLs, and focus on creating high-quality, valuable content for your readers.

4. Engage with Your Community: Encourage reader interaction through comments, social media, and email newsletters. Respond to comments promptly and use the feedback to generate ideas for future posts.

5. Backup Your Data: Regularly backup your blog content and database. While GitHub provides version control for your code, consider additional backup solutions for your images and any dynamic content.

6. Ethical AI Use: As you integrate AI into your blogging workflow, be transparent with your readers about its use. Consider adding a disclaimer to AI-generated or AI-assisted posts.

7. Accessibility: Ensure your blog is accessible to all users. Use proper heading structures, provide alt text for images, and consider implementing keyboard navigation.

8. Analytics: Implement analytics tools like Google Analytics or Plausible to gain insights into your audience and popular content. Use this data to inform your content strategy.

9. Monetization: If you're interested in monetizing your blog, consider options like affiliate marketing, sponsored content, or creating digital products. Ensure any monetization strategies align with your blog's purpose and audience.

10. Legal Compliance: Familiarize yourself with relevant laws and regulations, such as GDPR for handling user data or disclosure requirements for affiliate links.

By following these best practices and leveraging the power of Jekyll, Netlify, and AI, you've created a robust, efficient, and cutting-edge blogging platform. Your setup allows for rapid content creation, easy deployment, and ongoing optimization, all while maintaining control over your data and infrastructure.

Remember that blogging is as much about the journey as it is about the destination. Continuously experiment with new ideas, engage with your readers, and most importantly, enjoy the process of sharing your knowledge and experiences with the world.

As you continue to develop your blog, don't hesitate to dive deeper into each of these areas. The combination of static site generators, serverless functions, and AI-powered tools opens up endless possibilities for creating unique and engaging web experiences.

Happy blogging, and may your Jekyll-Netlify-AI powered blog bring value to both you and your readers for years to come!


