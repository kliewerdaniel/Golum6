---
layout: home
title: Enhancing Your Jekyll Blog with AI-Generated Persona Comments
date: 2024-09-15T12:30:38.348Z
---
## Introduction

In this guide, we'll explore how to enhance your Jekyll blog with AI-generated comments using various personas. This approach helps you gain diverse perspectives on your writing, including critical ones, and creates a more engaging journaling experience. We'll use locally-hosted large language models (LLMs) to generate these comments, providing a unique way to reflect on your blog posts or journal entries.

## Part 1: Setting Up Your Environment

### 1.1 Prerequisites

Ensure you have the following set up:

- A Jekyll blog (refer to the previous guide for setup instructions)
- Docker installed on your system
- OpenWebUI and Ollama set up (as described in the earlier guide)

### 1.2 Creating a Python Environment

Create a new virtual environment for our Python scripts:

```bash
python -m venv blog_env
source blog_env/bin/activate  # On Windows, use `blog_env\Scripts\activate`
pip install requests frontmatter
```

## Part 2: Defining Personas

Create a file named `personas.py` with the following content:

```python
PERSONAS = [
    {
        "name": "Critical Thinker",
        "description": "Analytical and skeptical, always questioning assumptions."
    },
    {
        "name": "Empathetic Listener",
        "description": "Focuses on emotional aspects and personal experiences."
    },
    {
        "name": "Devil's Advocate",
        "description": "Presents counterarguments to challenge ideas."
    },
    {
        "name": "Optimistic Visionary",
        "description": "Sees potential and positive outcomes in every situation."
    },
    {
        "name": "Pragmatic Planner",
        "description": "Focuses on practical implications and next steps."
    }
]
```

## Part 3: Generating Persona Comments

Create a file named `generate_comments.py`:

```python
import requests
import json
import random
from personas import PERSONAS

def generate_comment(post_content, persona):
    url = "http://localhost:11434/api/generate"
    prompt = f"""As a {persona['name']}, described as '{persona['description']}', 
    write a comment on the following blog post:

    {post_content}

    Keep the comment under 150 words and stay in character. Be insightful and specific."""

    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]

def generate_comments_for_post(post_content, num_comments=3):
    comments = []
    selected_personas = random.sample(PERSONAS, num_comments)
    for persona in selected_personas:
        comment = generate_comment(post_content, persona)
        comments.append({
            "persona": persona['name'],
            "comment": comment
        })
    return comments

# Example usage
post_content = """
Your blog post content here...
"""

comments = generate_comments_for_post(post_content)
for comment in comments:
    print(f"\n{comment['persona']}:")
    print(comment['comment'])
```

## Part 4: Integrating Comments into Jekyll Posts

### 4.1 Modifying Post Generation

Update your post generation script to include AI-generated comments. Create a file named `create_post_with_comments.py`:

```python
import frontmatter
from datetime import datetime
from generate_comments import generate_comments_for_post

def create_post_with_comments(title, content):
    post = frontmatter.Post(content)
    post['layout'] = 'post'
    post['title'] = title
    post['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate AI comments
    comments = generate_comments_for_post(content)
    post['ai_comments'] = comments

    filename = f"_posts/{datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"

    with open(filename, 'wb') as f:
        frontmatter.dump(post, f)

    print(f"Blog post with AI comments saved as {filename}")

# Example usage
title = "Reflections on Personal Growth"
content = """
Your blog post content here...
"""

create_post_with_comments(title, content)
```

### 4.2 Displaying AI Comments in Jekyll

To display the AI-generated comments in your Jekyll blog, you'll need to modify your post layout. Edit your `_layouts/post.html` file to include a section for AI comments:

```html
---
layout: default
---
<article class="post">
  <h1>{{ page.title }}</h1>
  <div class="entry">
    {{ content }}
  </div>

  {% if page.ai_comments %}
  <h2>AI-Generated Perspectives</h2>
  <div class="ai-comments">
    {% for comment in page.ai_comments %}
    <div class="ai-comment">
      <h3>{{ comment.persona }}</h3>
      <p>{{ comment.comment }}</p>
    </div>
    {% endfor %}
  </div>
  {% endif %}
</article>
```

## Part 5: Enhancing the Commenting System

### 5.1 Adding Sentiment Analysis

To gain more insights from the AI-generated comments, let's add sentiment analysis. First, install the required library:

```bash
pip install textblob
```

Then, update `generate_comments.py` to include sentiment analysis:

```python
from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0.1:
        return "Positive"
    elif sentiment < -0.1:
        return "Negative"
    else:
        return "Neutral"

def generate_comments_for_post(post_content, num_comments=3):
    comments = []
    selected_personas = random.sample(PERSONAS, num_comments)
    for persona in selected_personas:
        comment = generate_comment(post_content, persona)
        sentiment = analyze_sentiment(comment)
        comments.append({
            "persona": persona['name'],
            "comment": comment,
            "sentiment": sentiment
        })
    return comments
```

Update your Jekyll layout to display the sentiment:

```html
<div class="ai-comment">
  <h3>{{ comment.persona }} <span class="sentiment">({{ comment.sentiment }})</span></h3>
  <p>{{ comment.comment }}</p>
</div>
```

## Part 6: Analyzing Trends Across Multiple Posts

Create a new file named `analyze_trends.py` to analyze trends across multiple posts:

```python
import os
import frontmatter
from collections import Counter
from textblob import TextBlob

def analyze_posts(directory="_posts"):
    all_comments = []
    sentiment_trends = []
    persona_frequencies = Counter()

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r') as f:
                post = frontmatter.load(f)
                if 'ai_comments' in post.metadata:
                    for comment in post.metadata['ai_comments']:
                        all_comments.append(comment['comment'])
                        sentiment_trends.append(comment['sentiment'])
                        persona_frequencies[comment['persona']] += 1

    # Overall sentiment analysis
    overall_sentiment = TextBlob(" ".join(all_comments)).sentiment.polarity
    
    # Most frequent words
    words = [word for comment in all_comments for word in comment.split()]
    word_frequencies = Counter(words).most_common(10)

    return {
        "overall_sentiment": overall_sentiment,
        "sentiment_trends": Counter(sentiment_trends),
        "persona_frequencies": persona_frequencies,
        "common_words": word_frequencies
    }

# Example usage
trends = analyze_posts()
print("Overall Sentiment:", trends["overall_sentiment"])
print("\nSentiment Trends:", trends["sentiment_trends"])
print("\nPersona Frequencies:", trends["persona_frequencies"])
print("\nMost Common Words:", trends["common_words"])
```

## Conclusion

By integrating AI-generated comments from various personas into your Jekyll blog, you've created a powerful tool for self-reflection and personal growth. This system allows you to:

1. Gain diverse perspectives on your thoughts and ideas
2. Challenge your assumptions and biases
3. Track your personal growth and changing perspectives

Feel free to refine the personas, adjust the number of comments generated, or experiment with different LLMs as you continue using this AI-enhanced journaling system.


-﻿-------------

Hey folks! 👋 In this post, I’ll walk you through a cool project I’ve been working on: adding AI-generated comments to my Jekyll blog using different personas. This adds a unique layer of self-reflection and feedback to my posts, with AI playing various roles like the “Critical Thinker” or the “Optimistic Visionary.” You can try this out for journaling or blogging, and it's all powered by locally-hosted large language models (LLMs).

### 🔧 Part 1: Setting Up Your Environment

**1.1 Prerequisites**  
You’ll need:
- A Jekyll blog (if you don't have one, there are tons of guides to set it up).
- Docker installed on your machine.
- OpenWebUI and Ollama set up (this post assumes you already have them from a previous setup guide).

**1.2 Creating a Python Environment**  
We’ll be using Python to interact with the LLMs. First, create a new virtual environment for the project:

```bash
python -m venv blog_env
source blog_env/bin/activate  # (On Windows, use blog_env\Scripts\activate)
pip install requests frontmatter
```

### 🎭 Part 2: Defining Personas

Create a Python file named `personas.py`. This file will hold our predefined personas:

```python
PERSONAS = [
    { "name": "Critical Thinker", "description": "Analytical and skeptical, always questioning assumptions." },
    { "name": "Empathetic Listener", "description": "Focuses on emotional aspects and personal experiences." },
    { "name": "Devil's Advocate", "description": "Presents counterarguments to challenge ideas." },
    { "name": "Optimistic Visionary", "description": "Sees potential and positive outcomes in every situation." },
    { "name": "Pragmatic Planner", "description": "Focuses on practical implications and next steps." }
]
```

### 💬 Part 3: Generating AI Comments

Now, let's create a script to generate comments based on the personas. Create a file called `generate_comments.py`:

```python
import requests
import random
from personas import PERSONAS

def generate_comment(post_content, persona):
    url = "http://localhost:11434/api/generate"
    prompt = f"As a {persona['name']} ({persona['description']}), comment on this post:\n\n{post_content}"
    data = { "model": "llama2", "prompt": prompt, "stream": False }
    response = requests.post(url, json=data)
    return response.json()["response"]

def generate_comments_for_post(post_content, num_comments=3):
    selected_personas = random.sample(PERSONAS, num_comments)
    return [{ "persona": p['name'], "comment": generate_comment(post_content, p) } for p in selected_personas]

# Example usage
comments = generate_comments_for_post("Your blog post content here...")
for comment in comments:
    print(f"{comment['persona']}: {comment['comment']}")
```

### 🛠️ Part 4: Integrating Comments into Jekyll Posts

Modify your post-generation script to include AI comments. Create `create_post_with_comments.py`:

```python
import frontmatter
from datetime import datetime
from generate_comments import generate_comments_for_post

def create_post_with_comments(title, content):
    post = frontmatter.Post(content)
    post['layout'] = 'post'
    post['title'] = title
    post['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    post['ai_comments'] = generate_comments_for_post(content)

    filename = f"_posts/{datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
    with open(filename, 'wb') as f:
        frontmatter.dump(post, f)
    print(f"Blog post saved with AI comments at {filename}")
```

Then, update your Jekyll post layout (`_layouts/post.html`) to display the AI comments:

```html
{% if page.ai_comments %}
<h2>AI-Generated Comments</h2>
{% for comment in page.ai_comments %}
  <div>
    <h3>{{ comment.persona }}</h3>
    <p>{{ comment.comment }}</p>
  </div>
{% endfor %}
{% endif %}
```

### 🔍 Part 5: Adding Sentiment Analysis

For deeper insights, we’ll analyze the sentiment of each AI-generated comment. Install TextBlob:

```bash
pip install textblob
```

Modify `generate_comments.py` to include sentiment analysis:

```python
from textblob import TextBlob

def analyze_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    return "Positive" if sentiment > 0.1 else "Negative" if sentiment < -0.1 else "Neutral"

def generate_comments_for_post(post_content, num_comments=3):
    selected_personas = random.sample(PERSONAS, num_comments)
    comments = []
    for persona in selected_personas:
        comment = generate_comment(post_content, persona)
        sentiment = analyze_sentiment(comment)
        comments.append({ "persona": persona['name'], "comment": comment, "sentiment": sentiment })
    return comments
```

Now update the Jekyll layout to display the sentiment next to each comment:

```html
<h3>{{ comment.persona }} ({{ comment.sentiment }})</h3>
```

### 🧠 Part 6: Trend Analysis Across Multiple Posts

Want to analyze trends across your blog? Let’s write a script to analyze all AI comments across posts. Create `analyze_trends.py`:

```python
import os
import frontmatter
from collections import Counter

def analyze_posts(directory="_posts"):
    comments = []
    sentiment_trends = []
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r') as f:
                post = frontmatter.load(f)
                if 'ai_comments' in post.metadata:
                    for comment in post.metadata['ai_comments']:
                        comments.append(comment['comment'])
                        sentiment_trends.append(comment['sentiment'])
    return { "total_comments": len(comments), "sentiment_trends": Counter(sentiment_trends) }

# Example usage
trends = analyze_posts()
print("Total Comments:", trends["total_comments"])
print("Sentiment Trends:", trends["sentiment_trends"])
```

### 📊 Part 7: Reflection Dashboard

For a more interactive experience, create a reflection dashboard on your Jekyll site. Start by creating `reflection.md` in your site root:

```markdown
---
layout: page
title: Reflection Dashboard
permalink: /reflection/
---

<div id="reflection-dashboard"></div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// JS to populate the dashboard with trend data
</script>
```

Then, write a Jekyll plugin to generate the trend data:

```ruby
require 'json'
require_relative '../analyze_trends'

module Jekyll
  class TrendDataGenerator < Generator
    def generate(site)
      trends = analyze_posts()
      File.write('assets/trend_data.json', JSON.generate(trends))
    end
  end
end
```

The plugin will run at build time and generate `trend_data.json`. You can then load this data into your reflection dashboard with JavaScript.

### 🔄 Part 8: Journaling Workflow

Here’s a simple workflow you can follow:
1. Write your blog post.
2. Run `create_post_with_comments.py` to generate AI comments.
3. Review the AI-generated comments and reflect on them.
4. Analyze trends across your posts via the dashboard.
5. Set goals and track your personal growth over time.

---

That’s it! If you’re into reflective writing or journaling, this system is a great way to get diverse AI-generated feedback on your thoughts. Feel free to tweak the personas, the number of comments, or even try different LLMs. Let me know if you try it out or have any questions!
