---
layout: post
title: Updating Your Jekyll Blog to Use Anthropic API
date: 2024-09-13T23:51:46.803Z
---
'''# Updating Your Jekyll Blog to Use Anthropic API
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
That's it! Your Jekyll blog is now updated to use the Anthropic API for AI-enhanced content generation. The key changes are in the `ai_content_generator.py` script, where we've replaced the Ollama-specific code with Anthropic API calls. Here are some additional points to consider and potential enhancements:
## 11. Error Handling and Logging
Enhance the `ai_content_generator.py` script with better error handling and logging:
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def generate_ai_content(prompt):
try:
response = client.completion(
prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
model="claude-2",
max_tokens_to_sample=300,
)
return response.completion
except anthropic.APIError as e:
logger.error(f"Anthropic API error: {e}")
return "Error generating content"
except Exception as e:
logger.error(f"Unexpected error: {e}")
return "Error generating content"

## 12. Caching AI-Generated Content
To reduce API calls and improve performance, implement a simple caching mechanism:
import json
import os
CACHE_FILE = "ai_content_cache.json"
def load_cache():
if os.path.exists(CACHE_FILE):
with open(CACHE_FILE, 'r') as f:
return json.load(f)
return {}
def save_cache(cache):
with open(CACHE_FILE, 'w') as f:
json.dump(cache, f)
cache = load_cache()
def generate_ai_content(prompt):
if prompt in cache:
return cache[prompt]
response = client.completion(...) # Your existing API call
cache[prompt] = response.completion
save_cache(cache)
return response.completion

## 13. Customizing AI Prompts
Create a configuration file (`ai_config.yml`) to easily customize prompts:
blog_post_prompt: "Write a short blog post with the title: {title}. The post should be informative and engaging, suitable for a technical audience."
comments_prompt: "Generate 3 short, diverse comments for the following blog post. Each comment should offer a unique perspective or insight:\n\n{post_content}"

Then update `ai_content_generator.py` to use these custom prompts:
import yaml
with open('ai_config.yml', 'r') as f:
ai_config = yaml.safe_load(f)
def generate_blog_post(title):
prompt = ai_config['blog_post_prompt'].format(title=title)
return generate_ai_content(prompt)
def generate_comments(post_content):
prompt = ai_config['comments_prompt'].format(post_content=post_content)
return generate_ai_content(prompt)
## 14. Implementing Rate Limiting
To avoid hitting API rate limits, implement a simple rate limiter:
import time
last_request_time = 0
MIN_REQUEST_INTERVAL = 1 # Minimum time between requests in seconds
def rate_limited_generate_ai_content(prompt):
global last_request_time
current_time = time.time()
if current_time - last_request_time < MIN_REQUEST_INTERVAL:
time.sleep(MIN_REQUEST_INTERVAL - (current_time - last_request_time))
content = generate_ai_content(prompt)
last_request_time = time.time()
return content
## 15. Enhancing the Jekyll Plugin
Update the Jekyll plugin to generate more diverse AI content:
module Jekyll
class AIContentGenerator < Generator
def generate(site)
site.posts.docs.each do |post|
next if post.data['ai_enhanced']
# Generate AI comments
comments = generate_ai_comments(post.data['title'])
post.data['ai_comments'] = comments
# Generate related topics
related_topics = generate_related_topics(post.content)
post.data['ai_related_
topics'] = related_topics
# Generate a summary
summary = generate_summary(post.content)
post.data['ai_summary'] = summary
# Mark the post as AI-enhanced
post.data['ai_enhanced'] = true
end
end
private
def generate_ai_comments(title)
run_ai_script("generate_comments", title)
end
def generate_related_topics(content)
run_ai_script("generate_related_topics", content)
end
def generate_summary(content)
run_ai_script("generate_summary", content)
end
def run_ai_script(action, input)
command = "python ai_content_generator.py #{action} \"#{input}\""
stdout, stderr, status = Open3.capture3(command)
if status.success?
stdout.strip
else
Jekyll.logger.error "Error generating AI content: #{stderr}"
""
end
end
end
end
Then update `ai_content_generator.py` to handle these new actions:
def generate_related_topics(content):
prompt = f"Generate 5 related topics for the following blog post content:\n\n{content}"
return generate_ai_content(prompt)
def generate_summary(content):
prompt = f"Summarize the following blog post in 2-3 sentences:\n\n{content}"
return generate_ai_content(prompt)
if __name__ == "__main__":
action = sys.argv[1]
input_text = sys.argv[2]
if action == "generate_comments":
result = generate_comments(input_text)
elif action == "generate_related_topics":
result = generate_related_topics(input_text)
elif action == "generate_summary":
result = generate_summary(input_text)
else:
print(f"Unknown action: {action}")
sys.exit(1)
print(result)
## 16. Updating Post Layout
Update your post layout (`_layouts/post.html`) to display the new AI-generated content:
<article class="post">
<!-- Existing post content -->
{% if page.ai_summary %}
<h2>AI-Generated Summary</h2>
<div class="ai-summary">
{{ page.ai_summary | markdownify }}
</div>
{% endif %}
{% if page.ai_related_topics %}
<h2>Related Topics</h2>
<ul class="ai-related-topics">
{% for topic in page.ai_related_topics %}
<li>{{ topic }}</li>
{% endfor %}
</ul>
{% endif %}
{% if page.ai_comments %}
<h2>AI-Generated Comments</h2>
<div class="ai-comments">
{{ page.ai_comments | markdownify }}
</div>
{% endif %}
</article>

## 17. Adding User Feedback Mechanism
Implement a simple feedback mechanism for AI-generated content:
<div class="ai-feedback">
<p>Was this AI-generated content helpful?</p>
<button onclick="sendFeedback('positive')">👍 Yes</button>
<button onclick="sendFeedback('negative')">👎 No</button>
</div>
<script>
function sendFeedback(type) {
fetch('/ai-feedback', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ type: type, postId: '{{ page.id }}' })
}).then(response => {
if (response.ok) {
alert('Thank you for your feedback!');
}
});
}
</script>
You'll need to implement a server-side endpoint to handle this feedback, which could be used to fine-tune your prompts or AI usage over time.
## 18. Implementing Content Moderation
To ensure the AI-generated content is appropriate for your blog, you can implement a content moderation step. Here's how you can extend your setup to include this:
## 18. Implementing Content Moderation
Update the `ai_content_generator.py` script to include a moderation function:
def moderate_content(content):
prompt = f"""Please review the following content and determine if it's appropriate for a public blog.
If it contains any inappropriate language, offensive content, or sensitive information, please flag it.
If the content is appropriate, return 'APPROVED'. If not, return 'FLAGGED' along with a brief explanation.
Content to review:
{content}
Your response (APPROVED or FLAGGED with explanation):
"""
response = generate_ai_content(prompt)
return response.strip().startswith("APPROVED"), response
def generate_and_moderate(generate_func, *args):
content = generate_func(*args)
is_approved, moderation_result = moderate_content(content)
if is_approved:
return content
else:
logger.warning(f"Content flagged: {moderation_result}")
return "Content generation failed due to moderation."
# Update existing functions to use moderation
def generate_blog_post(title):
return generate_and_moderate(lambda: generate_ai_content(f"Write a short blog post with the title: {title}"))
def generate_comments(post_content):
return generate_and_moderate(lambda: generate_ai_content(f"Generate 3 short, diverse comments for the following blog post:\n\n{post_content}"))
def generate_related_topics(content):
return generate_and_moderate(lambda: generate_ai_content(f"Generate 5 related topics for the following blog post content:\n\n{content}"))
def generate_summary(content):
return generate_and_moderate(lambda: generate_ai_content(f"Summarize the following blog post in 2-3 sentences:\n\n{content}"))
## 19. Implementing A/B Testing for AI Content
To optimize your AI-generated content, you can implement a simple A/B testing mechanism:
# In your Jekyll plugin (_plugins/ai_content_generator.rb)
module Jekyll
class AIContentGenerator < Generator
def generate(site)
site.posts.docs.each do |post|
next if post.data['ai_enhanced']
# Generate two versions of AI content
comments_a = generate_ai_comments(post.data['title'])
comments_b = generate_ai_comments(post.data['title'])
# Randomly choose which version to use
post.data['ai_comments'] = [comments_a, comments_b].sample
post.data['ab_test_version'] = post.data['ai_comments'] == comments_a ? 'A' : 'B'
# ... (rest of your AI content generation)
post.data['ai_enhanced'] = true
end
end
# ... (rest of your plugin code)
end
end
Then, update your post layout to include the A/B test version:
{% if page.ai_comments %}
<div class="ai-comments" data-ab-version="{{ page.ab_test_version }}">
{{ page.ai_comments | markdownify }}
</div>
{% endif %}
## 20. Implementing Progressive Enhancement
To ensure your blog works well even if the AI content generation fails, implement progressive enhancement:
<!-- In your post layout -->
<article class="post">
<!-- Original content -->
{{ content }}
<!-- AI-enhanced content -->
<div id="ai-content" style="display: none;">
{% if page.ai_summary %}
<h2>AI-Generated Summary</h2>
<div class="ai-summary">{{ page.ai_summary | markdownify }}</div>
{% endif %}
{% if page.ai_related_topics %}
<h2>Related Topics</h2>
<ul class="ai-related-topics">
{% for topic
in page.ai_related_topics %}
<li>{{ topic }}</li>
{% endfor %}
</ul>
{% endif %}
{% if page.ai_comments %}
<h2>AI-Generated Comments</h2>
<div class="ai-comments">{{ page.ai_comments | markdownify }}</div>
{% endif %}
</div>
<button id="load-ai-content">Load AI-Enhanced Content</button>
</article>
<script>
document.getElementById('load-ai-content').addEventListener('click', function() {
document.getElementById('ai-content').style.display = 'block';
this.style.display = 'none';
});
</script>
This approach allows users to choose whether to load the AI-generated content, improving initial page load times and providing a fallback if AI content generation fails.
## 21. Implementing Personalized Content Recommendations
You can use the Anthropic API to generate personalized content recommendations based on a user's reading history. Here's how you might implement this:
First, add a new function to `ai_content_generator.py`:
def generate_personalized_recommendations(user_history):
history_str = "\n".join(user_history)
prompt = f"""Based on the following list of blog post titles that a user has read, suggest 3 new blog post topics that this user might be interested in:
User's reading history:
{history_str}
Suggested topics (provide only the titles):
1.
2.
3.
"""
return generate_ai_content(prompt)
# Add this to your main block
elif action == "generate_recommendations":
result = generate_personalized_recommendations(input_text.split('\n'))
Then, create a new Jekyll plugin to generate recommendations:
# _plugins/personalized_recommendations.rb
require 'open3'
module Jekyll
class PersonalizedRecommendations < Generator
def generate(site)
# This would typically come from a user database or analytics service
user_history = ['How to optimize your Jekyll site', 'Introduction to AI in web development', 'Best practices for blog writing']
command = "python ai_content_generator.py generate_recommendations \"#{user_history.join('\n')}\""
stdout, stderr, status = Open3.capture3(command)
if status.success?
recommendations = stdout.strip.split("\n")
site.config['personalized_recommendations'] = recommendations
else
Jekyll.logger.error "Error generating recommendations: #{stderr}"
end
end
end
end

Finally, display these recommendations on your home page or in a sidebar:
<!-- index.html or _includes/sidebar.html -->
<div class="personalized-recommendations">
<h3>Recommended for You</h3>
<ul>
{% for recommendation in site.personalized_recommendations %}
<li>{{ recommendation }}</li>
{% endfor %}
</ul>
</div>
## 22. Implementing an AI-Powered Search Feature
You can use the Anthropic API to power a more intelligent search feature for your blog. Here's a basic implementation:
Add a new function to `ai_content_generator.py`:
def ai_powered_search(query, posts):
posts_str = "\n".join([f"Title: {post['title']}\nExcerpt: {post['excerpt']}" for post in posts])
prompt = f"""Given the following blog posts and a search query, return the titles of the 3 most relevant posts. If there are fewer than 3 relevant posts, return only the relevant ones.
Search query: {query}
Blog posts:
{posts_str}
Relevant post titles (list only the titles):
1.
2.
3.
"""
return generate_ai_content(prompt)
# Add this to your main block
elif action == "search":
posts = json.loads(sys.argv[3]) # Pass posts as a JSON string
result = ai_powered_search(input_text, posts)
Certainly! Let's continue with implementing the AI-powered search feature and add some more enhancements to your Jekyll blog.
## 22. Implementing an AI-Powered Search Feature (continued)
Now, let's create a Jekyll plugin to integrate this AI-powered search:
# _plugins/ai_search.rb
require 'open3'
require 'json'
module Jekyll
class AISearch < Liquid::Tag
def initialize(tag_name, text, tokens)
super
@query = text.strip
end
def render(context)
site = context.registers[:site]
posts = site.posts.docs.map { |post| { title: post.data['title'], excerpt: post.data['excerpt'] } }
command = "python ai_content_generator.py search \"#{@query}\" '#{posts.to_json.gsub("'", "\\'")}'"
stdout, stderr, status = Open3.capture3(command)
if status.success?
results = stdout.strip.split("\n")
"<ul>" + results.map { |result| "<li>#{result}</li>" }.join + "</ul>"
else
Jekyll.logger.error "Error in AI search: #{stderr}"
"<p>Search failed. Please try again later.</p>"
end
end
end
end
Liquid::Template.register_tag('ai_search', Jekyll::AISearch)

Now you can use this in your search results page:
<!-- search.html -->
<h1>Search Results</h1>
<p>You searched for: {{ page.search_term }}</p>
<h2>AI-Powered Results:</h2>
{% ai_search page.search_term %}

## 23. Implementing AI-Generated Meta Descriptions
To improve SEO, you can use the Anthropic API to generate meta descriptions for your posts. Add this function to `ai_content_generator.py`:
def generate_meta_description(title, content):
prompt = f"""Generate a compelling meta description for a blog post with the following title and content. The meta description should be under 160 characters and entice readers to click through to the article.
Title: {title}
Content: {content[:500]}...
Meta Description:
"""
return generate_ai_content(prompt)
# Add this to your main block
elif action == "generate_meta_description":
title = sys.argv[2]
content = sys.argv[3]
result = generate_meta_description(title, content)

Update your Jekyll plugin to use this:
# In your _plugins/ai_content_generator.rb
def generate(site)
site.posts.docs.each do |post|
next if post.data['ai_enhanced']
# ... (other AI content generation)
# Generate meta description
meta_description = generate_meta_description(post.data['title'], post.content)
post.data['description'] = meta_description
post.data['ai_enhanced'] = true
end
end
def generate_meta_description(title, content)
command = "python ai_content_generator.py generate_meta_description \"#{title}\" \"#{content[0..500]}\""
stdout, stderr, status = Open3.capture3(command)
if status.success?
stdout.strip
else
Jekyll.logger.error "Error generating meta description: #{stderr}"
""
end
end
## 24. Implementing AI-Generated Social Media Posts
To help promote your blog posts, you can use the Anthropic API to generate social media posts. Add this function to `ai_content_generator.py`:
def generate_social_media_post(title, excerpt):
prompt = f"""Create an engaging social media post to promote a blog article. The post should be suitable for Twitter (under 280 characters) and include relevant hashtags.
Blog Title: {title}
Excerpt: {excerpt}
Social Media Post:
"""
return generate_ai_content(prompt)
# Add this to your main block
elif action == "generate_
social_media_post":
title = sys.argv[2]
excerpt = sys.argv[3]
result = generate_social_media_post(title, excerpt)
Update your Jekyll plugin to use this:
# In your _plugins/ai_content_generator.rb
def generate(site)
site.posts.docs.each do |post|
next if post.data['ai_enhanced']
# ... (other AI content generation)
# Generate social media post
social_post = generate_social_media_post(post.data['title'], post.data['excerpt'])
post.data['social_media_post'] = social_post
post.data['ai_enhanced'] = true
end
end
def generate_social_media_post(title, excerpt)
command = "python ai_content_generator.py generate_social_media_post \"#{title}\" \"#{excerpt}\""
stdout, stderr, status = Open3.capture3(command)
if status.success?
stdout.strip
else
Jekyll.logger.error "Error generating social media post: #{stderr}"
""
end
end
## 25. Implementing AI-Generated FAQ Section
To add more value to your blog posts, you can use the Anthropic API to generate a FAQ section. Add this function to `ai_content_generator.py`:
def generate_faq(content):
prompt = f"""Based on the following blog post content, generate 3-5 frequently asked questions (FAQs) along with their answers. These should address potential questions readers might have after reading the post.
Blog Content: {content[:1000]}...
FAQs:
1. Q:
A:
2. Q:
A:
3. Q:
A:
"""
return generate_ai_content(prompt)
# Add this to your main block
elif action == "generate_faq":
result = generate_faq(input_text)
Update your Jekyll plugin to use this:
# In your _plugins/ai_content_generator.rb
def generate(site)
site.posts.docs.each do |post|
next if post.data['ai_enhanced']
# ... (other AI content generation)
# Generate FAQ
faq = generate_faq(post.content)
post.data['ai_faq'] = faq
post.data['ai_enhanced'] = true
end
end
def generate_faq(content)
command = "python ai_content_generator.py generate_faq \"#{content[0..1000]}\""
stdout, stderr, status = Open3.capture3(command)
if status.success?
stdout.strip
else
Jekyll.logger.error "Error generating FAQ: #{stderr}"
""
end
end
## 26. Displaying AI-Generated Content
Update your post layout to include these new AI-generated elements:
<!-- _layouts/post.html -->
<article class="post h-entry" itemscope itemtype="http://schema.org/BlogPosting">
<!-- ... existing post content ... -->
{% if page.ai_faq %}
<h2>Frequently Asked Questions</h2>
<div class="ai-faq">
{{ page.ai_faq | markdownify }}
</div>
{% endif %}
{% if page.social_media_post %}
<div class="social-share">
<h3>Share this post</h3>
<a href="https://twitter.com/intent/tweet?text={{ page.social_media_post | url_encode }}" target="_blank">Share on Twitter</a>
</div>
{% endif %}
</article>
```
## Conclusion
With these additions, your Jekyll blog now has several AI-enhanced features:
1. AI-generated comments
2. AI-generated related topics
3. AI-generated summaries
4. Content moderation
5. A/B testing for AI content
6. Personalized content recommendations
7. AI-powered search
8. AI-generated meta descriptions
9. AI-generated social media posts
10. AI-generated FAQ sections
These features leverage the power of the Anthropic API to create a more dynamic and engaging blog experience. Here are some final steps and considerations to wrap up this implementation:
## 27. Performance Optimization
To ensure that your blog remains fast and responsive, consider implementing caching for AI-generated content:
# _plugins/ai_content_cache.rb
require 'yaml'
module Jekyll
class AIContentCache
def self.load
if File.exist?('_data/ai_content_cache.yml')
YAML.load_file('_data/ai_content_cache.yml')
else
{}
end
end
def self.save(cache)
File.write('_data/ai_content_cache.yml', cache.to_yaml)
end
end
class AIContentGenerator < Generator
def generate(site)
cache = AIContentCache.load
site.posts.docs.each do |post|
cache_key = post.path + post.date.to_s
if cache.key?(cache_key)
post.data.merge!(cache[cache_key])
else
# Generate AI content as before
# ...
cache[cache_key] = {
'ai_comments' => post.data['ai_comments'],
'ai_related_topics' => post.data['ai_related_topics'],
'ai_summary' => post.data['ai_summary'],
'ai_faq' => post.data['ai_faq'],
'social_media_post' => post.data['social_media_post']
}
end
end
AIContentCache.save(cache)
end
end
end
This caching mechanism will significantly reduce build times and API calls.
## 28. Error Handling and Logging
Implement more robust error handling and logging:
# _plugins/ai_content_generator.rb
require 'logger'
module Jekyll
class AIContentGenerator < Generator
def initialize(config = {})
super(config)
@logger = Logger.new(STDOUT)
@logger.level = Logger::INFO
end
def generate(site)
site.posts.docs.each do |post|
begin
# AI content generation logic
rescue => e
@logger.error "Error generating AI content for post #{post.path}: #{e.message}"
@logger.error e.backtrace.join("\n")
end
end
end
end
end
## 29. Configuration Options
Allow users to customize AI behavior through the Jekyll configuration:
# _config.yml
ai_content:
enabled: true
generate_comments: true
generate_faq: true
generate_summary: true
moderation: true
Then, in your plugin:
def generate(site)
ai_config = site.config['ai_content'] || {}
return unless ai_config['enabled']
site.posts.docs.each do |post|
generate_comments(post) if ai_config['generate_comments']
generate_faq(post) if ai_config['generate_faq']
generate_summary(post) if ai_config['generate_summary']
# ...
end
end
## 30. Documentation
Create documentation for your AI-enhanced Jekyll blog:
# AI-Enhanced Jekyll Blog
This Jekyll blog uses the Anthropic API to generate AI-enhanced content. Here's what you need to know:
## Setup
1. Install required gems: `bundle install`
2. Set up your Anthropic API key: `export ANTHROPIC_API_KEY=your_key_here`
3. Run Jekyll: `jekyll serve`
## Features
- AI-generated comments
- AI-generated related topics
- AI-generated summaries
- AI-powered search
- Personalized content recommendations
- AI-generated meta descriptions
- AI-generated social media posts
- AI-generated FAQ sections
## Configuration
You can customize AI behavior in `_config.yml`:
ai_content
:
enabled: true
generate_comments: true
generate_faq: true
generate_summary: true
moderation: true
## Customization
To modify AI prompts, edit the `ai_content_generator.py` file.
## Troubleshooting
If you encounter issues:
1. Check your Anthropic API key is set correctly
2. Ensure all required Python packages are installed
3. Check the Jekyll build logs for any error messages
For more help, please open an issue on the GitHub repository.
## 31. Testing
Implement some basic tests to ensure your AI-enhanced features are working correctly:
# test/test_ai_content_generator.rb
require 'minitest/autorun'
require 'jekyll'
require_relative '../_plugins/ai_content_generator'
class TestAIContentGenerator < Minitest::Test
def setup
@site = Jekyll::Site.new(Jekyll.configuration({
"source" => ".",
"destination" => "./
_site",
}))
@generator = Jekyll::AIContentGenerator.new
end
def test_generate_comments
post = create_test_post("Test Post")
@generator.generate_comments(post)
assert post.data.key?('ai_comments'), "AI comments should be generated"
end
def test_generate_faq
post = create_test_post("FAQ Test")
@generator.generate_faq(post)
assert post.data.key?('ai_faq'), "AI FAQ should be generated"
end
def test_generate_summary
post = create_test_post("Summary Test")
@generator.generate_summary(post)
assert post.data.key?('ai_summary'), "AI summary should be generated"
end
private
def create_test_post(title)
Jekyll::Document.new(
File.join(Dir.pwd, "_posts/2023-01-01-test-post.md"),
{ :site => @site, :collection => @site.posts }
).tap do |doc|
doc.data['title'] = title
doc.content = "This is a test post content."
end
end
end
Run these tests with `ruby test/test_ai_content_generator.rb`.
## 32. Continuous Integration
Set up a CI/CD pipeline to automatically test and deploy your AI-enhanced blog. Here's an example using GitHub Actions:

# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
test:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v2
- name: Set up Ruby
uses: ruby/setup-ruby@v1
with:
ruby-version: 3.0.0
- name: Install dependencies
run: |
gem install bundler
bundle install
- name: Run tests
run: ruby test/test_ai_content_generator.rb
- name: Build site
run: bundle exec jekyll build
env:
ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

## 33. Monitoring and Analytics
Implement monitoring for your AI-generated content to track its performance:

// assets/js/ai-analytics.js
function trackAIContentInteraction(type) {
if (typeof gtag !== 'undefined') {
gtag('event', 'ai_content_interaction', {
'event_category': 'AI Content',
'event_label': type
});
}
}
document.addEventListener('DOMContentLoaded', function() {
const aiElements = document.querySelectorAll('.ai-comments, .ai-faq, .ai-summary');
aiElements.forEach(function(el) {
el.addEventListener('click', function() {
trackAIContentInteraction(el.className);
});
});
});

Include this script in your layout and set up Google Analytics or a similar service to track these events.
## 34. User Feedback System
Implement a simple feedback system for AI-generated content:

<!-- _includes/ai_feedback.html -->
<div class="ai-feedback" data-type="{{ include.type }}">
<p>Was this AI-generated {{ include.type }} helpful?</p>
<button onclick="submitAIFeedback('{{ include.type }}', 'positive')">👍 Yes</button>
<button onclick="submitAIFeedback('{{ include.type }}', 'negative')">👎 No</button>
</div>
<script>
function submitAIFeedback(type, sentiment) {
fetch('/ai-feedback', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ type: type, sentiment: sentiment })
}).then(response => {
if (response.ok) {
alert('Thank you for your feedback!');
}
});
}
</
script>

Include this feedback component in your post layout:

<!-- _layouts/post.html -->
{% if page.ai_comments %}
<h2>AI-Generated Comments</h2>
<div class="ai-comments">{{ page.ai_comments | markdownify }}</div>
{% include ai_feedback.html type="comments" %}
{% endif %}
{% if page.ai_faq %}
<h2>Frequently Asked Questions</h2>
<div class="ai-faq">{{ page.ai_faq | markdownify }}</div>
{% include ai_feedback.html type="faq" %}
{% endif %}

## 35. Final Touches
1. Update your `README.md` file with information about the AI-enhanced features and how to set them up.
2. Create a CHANGELOG.md file to track changes and new AI features.
3. Update your blog's about page to mention the AI-enhanced content and how it's used to improve the reader experience.
4. Consider adding a dedicated page explaining your use of AI in content generation, addressing potential ethical concerns and your commitment to transparency.
## Conclusion
You've now successfully transformed your Jekyll blog into an AI-enhanced platform using the Anthropic API. This setup provides:
1. AI-generated comments, FAQs, summaries, and related topics
2. AI-powered search functionality
3. Personalized content recommendations
4. AI-generated meta descriptions and social media posts
5. Content moderation
6. A/B testing capabilities
7. Performance optimizations through caching
8. Error handling and logging
9. Customizable configuration options
10. Testing and continuous integration
11. Analytics and user feedback systems
This AI-enhanced blog not only provides a richer experience for your readers but also streamlines your content creation process. Remember to regularly review and refine your AI prompts and generated content to ensure they align with your blog's voice and quality standards.
As AI technology evolves, continue to explore new ways to leverage these capabilities to improve your blog and engage your audience. Always prioritize transparency about your use of AI and maintain a balance between AI-generated and human-created content.
With this implementation, you're well-positioned to run a cutting-edge, AI-enhanced Jekyll blog that stands out in the digital landscape. Happy blogging!

'﻿''