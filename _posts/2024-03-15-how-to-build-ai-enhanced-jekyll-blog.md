---
layout: post
title: "Building an AI-Enhanced Jekyll Blog with Netlify CMS and Docker: A Step-by-Step Guide"
date: 2024-09-11T23:51:46.803Z
---

# Building an AI-Enhanced Jekyll Blog with Netlify CMS and Docker: A Step-by-Step Guide

In this comprehensive guide, we'll walk through the process of setting up a Jekyll blog enhanced with AI capabilities, using Netlify CMS for content management and Docker for local development. This setup provides a powerful, flexible platform for creating and managing content, with the added benefit of AI-driven features.

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
         - {label: "Categories", name: "categories", widget: "list"}
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

1. Install the Ollama CLI tool for local AI model deployment. Follow the instructions at [Ollama](https://ollama.com/) for your operating system.
2. Create a script to interact with Ollama for content generation. Save this as `ai_content_generator.py` in your project root:

   ```python
   import subprocess
   import sys

   def generate_ai_content(prompt):
       result = subprocess.run(['ollama', 'run', 'llama2', prompt], capture_output=True, text=True)
       return result.stdout

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
   ```

3. Integrate the AI content generator into your Jekyll build process by creating a plugin. Create a new file `_plugins/ai_content_generator.rb`:

   ```ruby
   require 'open3'

   module Jekyll
     class AIContentGenerator < Generator
       def generate(site)
         site.posts.docs.each do |post|
           next if post.data['ai_enhanced']

           # Generate AI comments
           comments = generate_ai_comments(post.data['title'])
           post.data['ai_comments'] = comments

           # Mark the post as AI-enhanced
           post.data['ai_enhanced'] = true
         end
       end

       private

       def generate_ai_comments(title)
         command = "python ai_content_generator.py \"#{title}\""
         stdout, stderr, status = Open3.capture3(command)
         
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

4. Update your post layout to display AI-generated comments. In `_layouts/post.html`, add:

   ```html
    {% raw %}
    {% if page.ai_comments %}
   <h2>AI-Generated Comments</h2>
   <div class="ai-comments">
     {{ page.ai_comments | markdownify }}
   </div>
   {% endif %}
   {% endraw %}
   ```

## Step 5: Configure for Netlify Deployment

1. Create a `netlify.toml` file in your project root:

   ```toml
   [build]
     command = "jekyll build"
     publish = "_site"

   [build.environment]
     JEKYLL_ENV = "production"
   ```

2. Create a `.ruby-version` file in your project root with the content:

   ```
   3.0.0
   ```

3. Update your `Gemfile` to include the webrick gem (required for Ruby 3.0+):

   ```ruby
   gem "webrick", "~> 1.7"
   ```

4. Run `bundle install` to update your dependencies.

## Step 6: Run Locally with Docker

To run your AI-enhanced Jekyll blog locally, build and start the Docker container:

```bash
docker-compose up --build
```

Access your blog at [http://localhost:4000](http://localhost:4000) and the Netlify CMS admin panel at [http://localhost:4000/admin](http://localhost:4000/admin).

## Step 7: Deploy to Netlify

1. Push your repository to GitHub.
2. Log in to Netlify and click "New site from Git".
3. Choose your repository and configure the build settings:
   - Build command: `jekyll build`
   - Publish directory: `_site`
4. Click "Deploy site" and wait for the initial deployment to complete.
5. Set up Netlify Identity for authentication:
   - Go to your site's settings in Netlify
   - Navigate to "Identity" and click "Enable Identity"
   - Under "Registration preferences", choose "Invite only"
   - Scroll down to "Services" and click "Enable Git Gateway"
6. Invite yourself as a user:
   - Go to the "Identity" tab
   - Click "Invite users"
   - Enter your email address and send the invitation
7. Accept the invitation and set up your account.

## Step 8: Final Touches

1. Update your `_config.yml` file to include the base URL of your Netlify site:

   ```yaml
   url: "https://your-site-name.netlify.app" # Replace with your actual Netlify URL
   ```

2. Add the Netlify Identity widget to your main layout file (usually `_layouts/default.html`):

   ```html
   <script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
   ```

3. Commit and push these changes to your GitHub repository.

## Conclusion

Congratulations! You now have a fully functional AI-enhanced Jekyll blog set up with Netlify CMS and Docker. This setup provides a powerful platform for creating and managing content, with the added benefit of AI-driven features like automated comment generation.

Here's a summary of what we've accomplished:

- Set up a basic Jekyll blog
- Dockerized the blog for easy local development
- Integrated Netlify CMS for content management
- Added AI capabilities using Ollama for generating comments
- Configured the blog for Netlify deployment
- Set up Netlify Identity for secure admin access

Remember to fine-tune the AI prompts and responses to better fit your blog's tone and style. As you continue to develop your blog, you can expand the AI capabilities to include features like content summarization, SEO optimization suggestions, or even AI-assisted content creation.

Some potential next steps to consider:

- Customize the blog's theme and layout to match your personal style
- Implement SEO best practices
- Set up a custom domain name
- Explore more advanced AI integrations, such as content recommendations or automated tagging

Happy blogging, and enjoy your new AI-enhanced Jekyll site!

