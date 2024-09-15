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
