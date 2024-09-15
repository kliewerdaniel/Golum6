---
layout: home
title: Enhancing Your Jekyll Blog with AI-Generated Persona Comments
date: 2024-09-15T12:30:38.348Z
---
## Introduction

In this guide, we'll explore how to enhance your Jekyll blog with AI-generated comments using various personas. This approach can help you gain diverse perspectives on your writing, including critical ones, and create a more engaging journaling experience. We'll use locally-hosted large language models (LLMs) to generate these comments, providing a unique way to reflect on your blog posts or journal entries.

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

### 5.2 Implementing a Reflection Prompt

To encourage self-reflection based on the AI comments, let's add a reflection prompt generator. Add the following function to `generate_comments.py`:

```python
def generate_reflection_prompt(comments):
    url = "http://localhost:11434/api/generate"
    comments_summary = "\n".join([f"{c['persona']}: {c['comment']}" for c in comments])
    prompt = f"""Based on the following AI-generated comments:

    {comments_summary}

    Generate a thought-provoking question for the author to reflect on. 
    The question should encourage deep thinking about the content and the perspectives provided."""

    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=data)
    return json.loads(response.text)["response"]
```

Update the `create_post_with_comments` function in `create_post_with_comments.py`:

```python
from generate_comments import generate_comments_for_post, generate_reflection_prompt

def create_post_with_comments(title, content):
    # ... (previous code)
    
    comments = generate_comments_for_post(content)
    post['ai_comments'] = comments
    
    reflection_prompt = generate_reflection_prompt(comments)
    post['reflection_prompt'] = reflection_prompt

    # ... (rest of the function)

# Example usage remains the same
```

Update your Jekyll layout (`_layouts/post.html`) to include the reflection prompt:

```html
{% if page.ai_comments %}
<h2>AI-Generated Perspectives</h2>
<div class="ai-comments">
  {% for comment in page.ai_comments %}
  <div class="ai-comment">
    <h3>{{ comment.persona }} <span class="sentiment">({{ comment.sentiment }})</span></h3>
    <p>{{ comment.comment }}</p>
  </div>
  {% endfor %}
</div>

{% if page.reflection_prompt %}
<div class="reflection-prompt">
  <h3>Reflection Prompt</h3>
  <p>{{ page.reflection_prompt }}</p>
</div>
{% endif %}
{% endif %}
```

## Part 6: Analyzing Trends Across Multiple Posts

To gain deeper insights from your blogging or journaling practice, let's create a script to analyze trends across multiple posts.

Create a new file named `analyze_trends.py`:

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

This script analyzes all your posts, providing insights into overall sentiment, sentiment trends, most active personas, and commonly used words across all AI-generated comments.

## Part 7: Creating a Reflection Dashboard

To visualize the trends and insights from your blog posts, let's create a simple dashboard using Jekyll.

Create a new file named `reflection.md` in your Jekyll site's root directory:

```markdown
---
layout: page
title: Reflection Dashboard
permalink: /reflection/
---

<div id="reflection-dashboard">
  <h2>Overall Sentiment</h2>
  <div id="overall-sentiment"></div>

  <h2>Sentiment Trends</h2>
  <div id="sentiment-trends"></div>

  <h2>Most Active Personas</h2>
  <div id="persona-frequencies"></div>

  <h2>Common Themes</h2>
  <div id="common-words"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// We'll add JavaScript to populate this dashboard in the next step
</script>
```

Now, create a new Jekyll plugin to generate the trend data. Create a file named `_plugins/trend_data_generator.rb`:

```ruby
require 'json'
require_relative '../analyze_trends'

module Jekyll
  class TrendDataGenerator < Generator
    def generate(site)
      trends = analyze_posts
      File.write('assets/trend_data.json', JSON.generate(trends))
    end
  end
end
```

This plugin will run the `analyze_posts` function and save the results as a JSON file.

Update the `reflection.md` file to include JavaScript that loads and displays this data:

```html
<script>
fetch('/assets/trend_data.json')
  .then(response => response.json())
  .then(data => {
    // Overall Sentiment
    document.getElementById('overall-sentiment').textContent = 
      `${(data.overall_sentiment * 100).toFixed(2)}% Positive`;

    // Sentiment Trends
    new Chart(document.getElementById('sentiment-trends'), {
      type: 'pie',
      data: {
        labels: Object.keys(data.sentiment_trends),
        datasets: [{
          data: Object.values(data.sentiment_trends)
        }]
      }
    });

    // Persona Frequencies
    new Chart(document.getElementById('persona-frequencies'), {
      type: 'bar',
      data: {
        labels: Object.keys(data.persona_frequencies),
        datasets: [{
          data: Object.values(data.persona_frequencies)
        }]
      }
    });

    // Common Words
    new Chart(document.getElementById('common-words'), {
      type: 'horizontalBar',
      data: {
        labels: data.common_words.map(pair => pair[0]),
        datasets: [{
          data: data.common_words.map(pair => pair[1])
        }]
      }
    });
  });
</script>
```

## Part 8: Implementing a Journaling Workflow

To make the most of this AI-enhanced blogging system, consider implementing the following journaling workflow:

1. **Write Your Post**: Start by writing your blog post or journal entry as usual.

2. **Generate AI Comments**: Use the `create_post_with_comments.py` script to generate AI-powered comments from various personas.

3. **Review and Reflect**: Read through the AI-generated comments and the reflection prompt. Take time to consider these different perspectives.

4. **Respond to Comments**: If a particular AI comment resonates with you or challenges your thinking, consider writing a response to it within your post.

5. **Update Your Post**: Based on your reflections and responses, you might want to update or expand your original post.

6. **Analyze Trends**: Regularly review the Reflection Dashboard to identify patterns in your writing and the AI-generated responses over time.

7. **Set Goals**: Use the insights from the dashboard to set goals for your personal growth or to identify areas you'd like to explore further in your writing.

## Conclusion

By integrating AI-generated comments from various personas into your Jekyll blog, you've created a powerful tool for self-reflection and personal growth. This system allows you to:

1. Gain diverse perspectives on your thoughts and ideas
2. Challenge your assumptions and biases
3. Identify patterns in your thinking over time
4. Engage in a form of dialogue with different viewpoints
5. Track your personal growth and changing perspectives

Remember that while the AI-generated comments can provide valuable insights, they are ultimately tools to enhance your own thinking and reflection. The real value comes from your engagement with these ideas and your commitment to personal growth.

As you continue to use this system, you may want to:

- Refine the personas or add new ones to explore different perspectives
- Adjust the number of comments generated for each post
- Experiment with different LLMs to see how they affect the quality and diversity of the generated comments
- Expand the trend analysis to include more sophisticated natural language processing techniques

By combining the power of static site generators like Jekyll with locally-hosted LLMs, you've created a unique and powerful journaling system. This approach allows you to leverage AI to enhance your writing and self-reflection while maintaining control over your data and the entire process.

