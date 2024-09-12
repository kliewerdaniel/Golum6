---
layout: post
title: Building an AI-Enhanced Jekyll Blog with Netlify CMS, Docker, and Ollama
date: 2024-09-11T23:51:46.803Z
---
# Building an AI-Enhanced Jekyll Blog with Netlify CMS, Docker, and Ollama
This guide provides step-by-step instructions to set up a Jekyll blog using Netlify CMS, Docker, Netlify for deployment, and Ollama for AI-enhanced content generation.
## Prerequisites
Make sure you have the following installed on your system:
- Git
- Docker and Docker Compose
- Ruby (version 3.0.0 or later)
- Bundler and Jekyll
- Node.js and npm
- Netlify CLI
- Ollama CLI tool
## Installation Steps
1. Install Git:
```
sudo apt-get update
sudo apt-get install git
```
2. Install Docker and Docker Compose: Follow the official Docker documentation for your OS.
3. Install Ruby using rbenv:
```
sudo apt-get install rbenv
rbenv install 3.0.0
rbenv global 3.0.0
```
4. Install Bundler and Jekyll:
```
gem install bundler jekyll
```
5. Install Node.js and npm:
```
sudo apt-get install nodejs npm
```
6. Install Netlify CLI:
```
npm install netlify-cli -g
```
7. Install Ollama: Follow the instructions at [Ollama](https://ollama.com/) for your operating system.
## Getting Started
1. Clone the Repository:
```
git clone https://github.com/kliewerdaniel/golum2.git
cd golum2
```
2. Run the Setup Script:
```
chmod +x golum.sh
./golum.sh
```
The script will set up your Jekyll blog with Netlify CMS, Docker, and now includes steps for Ollama integration.
## Ollama Integration
The setup script now includes steps to integrate Ollama for AI-enhanced content generation:
1. Create a Python script for AI content generation (`ai_content_generator.py`):
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
2. Create a Jekyll plugin to use the AI content generator (`_plugins/ai_content_generator.rb`):
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
## Using the Ollama Integration
After setting up the AI content generator and Jekyll plugin, you can now leverage AI-enhanced features in your blog:
1. AI-Generated Comments: The plugin will automatically generate AI comments for each blog post during the Jekyll build process.
2. Display AI Comments: Update your post layout (`_layouts/post.html`) to display the AI-generated comments:
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
3. Manual AI Content Generation: You can also use the AI content generator script directly:
```bash
python ai_content_generator.py "Your Blog Post Title"
```
This will generate a blog post and comments based on the given title.
## Next Steps
Once the setup is complete, you can:
1. Visit http://localhost:4000 to view your blog locally.
2. Use the Netlify CMS at http://localhost:4000/admin to manage content.
3. Commit and push changes to GitHub to trigger deployment on Netlify.
4. Experiment with different AI prompts by modifying the `ai_content_generator.py` script.
## Project Structure After Setup
```
my-blog/
├── _posts/
├── _site/
├── _plugins/
│ └── ai_content_generator.rb
├── admin/
│ ├── config.yml
│ └── index.html
├── assets/
│ └── uploads/
├── _config.yml
├── Dockerfile
├── docker-compose.yml
├── Gemfile
├── Gemfile.lock
├── .ruby-version
└── ai_content_generator.py
```
## Customization
1. Modify `_config.yml` for basic settings.
2. Edit or add templates in the `_layouts` and `_includes` directories.
3. Customize styles in the `assets/css` directory.
4. Adjust AI prompts in `ai_content_generator.py` to better fit your blog's tone and style.
## Troubleshooting
- Ensure all prerequisites, including Ollama, are correctly installed.
- Confirm the local Ruby version matches `.ruby-version` (3.0.0).
- Verify the Bundler version is compatible with Ruby 3.0.0.
- If AI content generation fails, check that Ollama is running and the `llama2` model is available.
## Deployment
1. Push changes to your GitHub repository.
2. Netlify will automatically detect changes and trigger a new build.
3. Once the build is complete, Netlify will deploy your site.
## Writing Blog Posts
You can create blog posts using the Netlify CMS, manually in the `_posts` directory, or use the AI content generator for inspiration.
### Manual Post Example
```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [category1, category2]
---
Your post content in Markdown goes here.
```
## Conclusion
By following this guide, you'll have a fully functional Jekyll blog integrated with Netlify CMS, Docker, Netlify deployment, and AI-enhanced features using Ollama. This setup provides a powerful platform for creating and managing content, with the added benefit of AI-driven capabilities.
For additional resources:
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Netlify CMS Documentation](https://www.netlifycms.org/docs/intro/)
- [Docker Documentation](https://docs.docker.com/)
- [Ollama Documentation](https://ollama.ai/docs)
Remember to experiment with the AI features and adjust them to best suit your blogging needs. You can expand the AI capabilities to include features like content summarization, SEO optimization suggestions, or even full AI-assisted content creation.
Happy blogging with your new AI-enhanced Jekyll site!
-enhanced Jekyll site!

------