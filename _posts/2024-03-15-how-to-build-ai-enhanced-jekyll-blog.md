---
layout: post
title: "How to Build an AI-Enhanced Jekyll Blog with Netlify CMS and Docker"
date: 2024-03-15 09:00:00 -0500
---

# Building an AI-Enhanced Jekyll Blog with Netlify CMS and Docker

In this guide, we'll walk through the process of setting up a Jekyll blog enhanced with AI capabilities, using Netlify CMS for content management and Docker for local development. This setup provides a powerful, flexible platform for creating and managing content, with the added benefit of AI-driven features.

## Prerequisites

Before we begin, ensure you have the following installed:

- Git
- Docker and Docker Compose
- Ruby (version 3.0.0 or higher)
- Bundler and Jekyll
- Node.js and npm
- Netlify CLI

## Step 1: Set Up the Basic Jekyll Blog

1. Create a new Jekyll site:
   ```bash
   jekyll new ai-enhanced-blog
   cd ai-enhanced-blog
   ```

2. Initialize Git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

## Step 2: Dockerize the Jekyll Blog

1. Create a `Dockerfile` in the root of your project:
   ```dockerfile
   FROM jekyll/jekyll:4.2.0
   WORKDIR /srv/jekyll
   COPY . .
   RUN bundle install
   CMD ["jekyll", "serve", "--force_polling", "-H", "0.0.0.0"]
   ```

2. Create a `docker-compose.yml` file:
   ```yaml
   version: '3'
   services:
     site:
       command: jekyll serve --force_polling
       image: jekyll/jekyll:4.2.0
       volumes:
         - .:/srv/jekyll
       ports:
         - 4000:4000
   ```

## Step 3: Set Up Netlify CMS

1. Create an `admin` folder in the root of your project.
2. Create `admin/config.yml`:
   ```yaml
   backend:
     name: git-gateway
     branch: main
   media_folder: "assets/uploads"
   collections:
     - name: "blog"
       label: "Blog"
       folder: "_posts"
       create: true
       slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
       fields:
         - {label: "Layout", name: "layout", widget: "hidden", default: "post"}
         - {label: "Title", name: "title", widget: "string"}
         - {label: "Publish Date", name: "date", widget: "datetime"}
         - {label: "Body", name: "body", widget: "markdown"}
   ```

3. Create `admin/index.html`:
   ```html
   <!doctype html>
   <html>
   <head>
     <meta charset="utf-8" />
     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
     <title>Content Manager</title>
   </head>
   <body>
     <script src="https://unpkg.com/netlify-cms@^2.0.0/dist/netlify-cms.js"></script>
     <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
   </body>
   </html>
   ```

## Step 4: Integrate AI Capabilities

1. Install the Ollama CLI tool for local AI model deployment.
2. Create a script to interact with Ollama for content generation:
   ```python
   import subprocess

   def generate_ai_content(prompt):
       result = subprocess.run(['ollama', 'run', 'llama2', prompt], capture_output=True, text=True)
       return result.stdout

   def generate_blog_post(title):
       prompt = f"Write a blog post with the title: {title}"
       return generate_ai_content(prompt)

   def generate_comments(post_content):
       prompt = f"Generate 3 diverse comments for the following blog post:\n\n{post_content}"
       return generate_ai_content(prompt)

   # Example usage
   title = "The Future of AI in Web Development"
   post_content = generate_blog_post(title)
   comments = generate_comments(post_content)

   print("Generated Blog Post:")
   print(post_content)
   print("\nGenerated Comments:")
   print(comments)
   ```

3. Save this as `ai_content_generator.py` in your project root.
4. Integrate the AI content generator into your Jekyll build process by creating a plugin. Create a new file `_plugins/ai_content_generator.rb`:
   ```ruby
   require 'open3'

   module Jekyll
     class AIContentGenerator < Generator
       def generate(site)
         site.posts.docs.each do |post|
           next if post.data['ai_enhanced']

           # Generate AI comments
           comments = generate_ai_comments(post.content)
           post.data['ai_comments'] = comments

           # Mark the post as AI-enhanced
           post.data['ai_enhanced'] = true
         end
       end

       private

       def generate_ai_comments(content)
         command = "python ai_content_generator.py"
         stdout, stderr, status = Open3.capture3(command, stdin_data: content)
         
         if status.success?
           stdout.strip
         else
           Jekyll.logger.error "Error generating AI comments: #{stderr}"
           ""
         end
       end
     end
   end
   ```

5. Update your post layout to display AI-generated comments. In `_layouts/post.html`, add:
   ```html
   {% if page.ai_comments %}
   <h2>AI-Generated Comments</h2>
   <div class="ai-comments">
     {{ page.ai_comments | markdownify }}
   </div>
   {% endif %}
   ```

## Step 5: Deploy to Netlify

1. Create a `netlify.toml` file in your project root:
   ```toml
   [build]
     command = "jekyll build"
     publish = "_site"

   [build.environment]
     JEKYLL_ENV = "production"
   ```

2. Initialize Netlify:
   ```bash
   netlify init
   ```

   Follow the prompts to connect your GitHub repository and set up continuous deployment.

## Step 6: Run Locally with Docker

To run your AI-enhanced Jekyll blog locally:

1. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```

2. Access your blog at [http://localhost:4000](http://localhost:4000) and the Netlify CMS admin panel at [http://localhost:4000/admin](http://localhost:4000/admin).

## Conclusion

You now have a powerful, AI-enhanced Jekyll blog set up with Netlify CMS and Docker. This setup allows for easy content management, local development, and AI-driven features like automated comment generation.

Remember to fine-tune the AI prompts and responses to better fit your blog's tone and style. As you continue to develop your blog, you can expand the AI capabilities to include features like content summarization, SEO optimization suggestions, or even AI-assisted content creation.

Happy blogging!