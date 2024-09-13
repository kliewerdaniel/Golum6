---
layout: home
title: Building an AI-Enhanced Jekyll Blog with Netlify CMS, Docker, and Ollama
date: 2024-09-12T15:26:46.465Z
---
# Guide to Set Up a Jekyll Blog with Netlify CMS, Docker, Netlify, and Ollama for AI-Enhanced Content Generation

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

### Install Git:
```bash
sudo apt-get update
sudo apt-get install git
```

### Install Docker and Docker Compose:
Follow the [official Docker documentation](https://docs.docker.com/get-docker/) for your OS.

### Install Ruby using rbenv:
```bash
sudo apt-get install rbenv
rbenv install 3.0.0
rbenv global 3.0.0
```

### Install Bundler and Jekyll:
```bash
gem install bundler jekyll
```

### Install Node.js and npm:
```bash
sudo apt-get install nodejs npm
```

### Install Netlify CLI:
```bash
npm install netlify-cli -g
```

### Install Ollama:
Follow the instructions at [Ollama](https://ollama.com/) for your operating system.

## Getting Started

### Clone the Repository:
```bash
git clone https://github.com/kliewerdaniel/golum2.git
cd golum2
```

### Run the Setup Script:
```bash
chmod +x golum.sh
./golum.sh
```
The script will set up your Jekyll blog with Netlify CMS, Docker, and now includes steps for Ollama integration.

## Ollama Integration

The setup script now includes steps to integrate Ollama for AI-enhanced content generation:

### Create a Python Script for AI Content Generation (`ai_content_generator.py`):
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

### Create a Jekyll Plugin to Use the AI Content Generator (`_plugins/ai_content_generator.rb`):
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

### AI-Generated Comments:
The plugin will automatically generate AI comments for each blog post during the Jekyll build process.

### Display AI Comments:
Update your post layout (`_layouts/post.html`) to display the AI-generated comments:
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

### Manual AI Content Generation:
You can also use the AI content generator script directly:
```bash
python ai_content_generator.py "Your Blog Post Title"
```
This will generate a blog post and comments based on the given title.

## Next Steps

Once the setup is complete, you can:
- Visit `http://localhost:4000` to view your blog locally.
- Use the Netlify CMS at `http://localhost:4000/admin` to manage content.
- Commit and push changes to GitHub to trigger deployment on Netlify.
- Experiment with different AI prompts by modifying the `ai_content_generator.py` script.

## Project Structure After Setup

```
my-blog/
├── _posts/
├── _site/
├── _plugins/
│   └── ai_content_generator.rb
├── admin/
│   ├── config.yml
│   └── index.html
├── assets/
│   └── uploads/
├── _config.yml
├── Dockerfile
├── docker-compose.yml
├── Gemfile
├── Gemfile.lock
├── .ruby-version
└── ai_content_generator.py
```

## Customization

- Modify `_config.yml` for basic settings.
- Edit or add templates in the `_layouts` and `_includes` directories.
- Customize styles in the `assets/css` directory.
- Adjust AI prompts in `ai_content_generator.py` to better fit your blog's tone and style.

## Troubleshooting

- Ensure all prerequisites, including Ollama, are correctly installed.
- Confirm the local Ruby version matches `.ruby-version` (3.0.0).
- Verify the Bundler version is compatible with Ruby 3.0.0.
- If AI content generation fails, check that Ollama is running and the llama2 model is available.

## Deployment

- Push changes to your GitHub repository.
- Netlify will automatically detect changes and trigger a new build.
- Once the build is complete, Netlify will deploy your site.

## Writing Blog Posts

You can create blog posts using the Netlify CMS, manually in the `_posts` directory, or use the AI content generator for inspiration.

### Manual Post Example:
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

### For additional resources:
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Netlify CMS Documentation](https://www.netlifycms.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Ollama Documentation](https://ollama.com/docs/)

### Additional Tips and Best Practices

- **Optimizing AI-Generated Content**:
  - Fine-tune prompts: Experiment with different prompts in the `ai_content_generator.py` script to get the best results for your blog's style and tone.
  - Human review: Always review and edit AI-generated content to ensure quality and accuracy.
  
- **Security Considerations**:
  - Ensure that API keys are stored securely and not exposed in your repository.

- **Performance Optimization**:
  - Implement caching for AI-generated content to reduce load times and API calls.

- **Extending AI Capabilities**:
  - Use AI to suggest SEO improvements, generate content ideas, or create AI-generated visuals.

- **Future Enhancements**:
  - Explore personalized content recommendations, AI-powered chatbots, voice integration, and multilingual support.

Happy blogging with your new AI-enhanced Jekyll site!
```