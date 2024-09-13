---
layout: post
title: Ultimate Guide Jekyll Blog with Netlify CMS, Docker, and AI Integration
date: 2024-09-13T22:33:28.510Z
---
## Introduction

This guide will walk you through setting up a Jekyll blog with Netlify CMS and Docker, then enhancing it with AI-driven content creation using Ollama. We'll start with the basic setup and then integrate advanced AI features.

## Prerequisites

- Git
- Docker & Docker Compose
- Ruby (3.0.0 or higher)
- Bundler & Jekyll
- Node.js & npm
- Netlify CLI

## Part 1: Basic Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/kliewerdaniel/golum2.git
cd golum3
```

### Step 2: Run the Setup Script

Make the script executable:

```bash
chmod +x golum.sh
```

Run the script:

```bash
./golum.sh
```

This script will:
- Set up a new Jekyll blog
- Create a local Git repository
- Build and run the Docker container
- Set up Netlify for deployment

### Step 3: Access Your Blog

- Local blog: http://localhost:4000
- Admin panel: http://localhost:4000/admin

## Part 2: AI Integration with Ollama

### Step 1: Install Ollama

Follow the installation instructions for Ollama on their official website.

### Step 2: Set Up Open WebUI for Ollama

Clone the Open WebUI repository:

```bash
git clone https://github.com/example/open-webui.git
cd open-webui
npm install
```

### Step 3: Configure Ollama

Create a configuration file `config.js`:

```javascript
const ollama = require('ollama-api');

ollama.initialize({
  apiKey: 'YOUR_API_KEY'
});

module.exports = ollama;
```

### Step 4: Create Content Generation Script

Create a file `generate-content.js`:

```javascript
const ollama = require('./config');
const fs = require('fs');
const path = require('path');

async function generateContent(prompt) {
  const response = await ollama.generate({ prompt });
  return response.text;
}

async function savePost(title, content) {
  const filename = `${new Date().toISOString().slice(0, 10)}-${title.replace(/\s+/g, '-').toLowerCase()}.md`;
  const filePath = path.join('_posts', filename);
  const frontMatter = `---
layout: post
title: "${title}"
date: ${new Date().toISOString()}
---
`;
  fs.writeFileSync(filePath, frontMatter + content);
}

async function createAIPost(prompt) {
  const content = await generateContent(prompt);
  await savePost(prompt, content);
  console.log(`Post created: ${prompt}`);
}

createAIPost('Write a blog post about the latest trends in AI');
```

### Step 5: Integrate with Jekyll

Update your Jekyll configuration to include the AI-generated posts:

```yaml
# _config.yml
include:
  - _posts
```

### Step 6: Set Up Automated Content Generation

Create a GitHub Action to run the content generation script periodically:

```yaml
# .github/workflows/generate-content.yml
name: Generate AI Content

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - run: npm install
    - run: node generate-content.js
    - name: Commit and push if changed
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
        git add -A
        git commit -m "Add AI-generated content" || exit 0
        git push
```

## Part 3: Enhancing AI Integration

### Step 7: Implement AI-Driven Comments

To simulate user interactions and provide diverse perspectives on your blog posts, you can use Ollama to generate AI-driven comments. Here's how to implement this feature:

1. Create a new file `generate-comments.js`:

```javascript
const ollama = require('./config');
const fs = require('fs');
const path = require('path');

async function generateComment(postContent, persona) {
  const prompt = `As ${persona}, write a thoughtful comment on the following blog post:\n\n${postContent}`;
  const response = await ollama.generate({ prompt });
  return response.text;
}

async function addCommentToPost(postPath, comment, persona) {
  const postContent = fs.readFileSync(postPath, 'utf8');
  const updatedContent = `${postContent}\n\n---\n\nComment from ${persona}:\n${comment}`;
  fs.writeFileSync(postPath, updatedContent);
}

async function generateCommentsForAllPosts() {
  const postsDir = path.join(__dirname, '_posts');
  const files = fs.readdirSync(postsDir);

  for (const file of files) {
    if (file.endsWith('.md')) {
      const postPath = path.join(postsDir, file);
      const postContent = fs.readFileSync(postPath, 'utf8');

      const personas = ['AI Researcher', 'Tech Enthusiast', 'Skeptical User'];
      for (const persona of personas) {
        const comment = await generateComment(postContent, persona);
        await addCommentToPost(postPath, comment, persona);
      }

      console.log(`Added AI-generated comments to ${file}`);
    }
  }
}

generateCommentsForAllPosts();
```

2. Update your GitHub Action to include comment generation:

```yaml
# .github/workflows/generate-content.yml
name: Generate AI Content and Comments

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight
  workflow_dispatch:  # Allow manual triggering

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - run: npm install
    - run: node generate-content.js
    - run: node generate-comments.js
    - name: Commit and push if changed
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
        git add -A
        git commit -m "Add AI-generated content and comments" || exit 0
        git push
```

### Step 8: Implement Content Summarization

To provide quick overviews of your blog posts, you can use Ollama to generate summaries:

1. Create a new file `generate-summaries.js`:
<﻿!--
```javascript
const ollama = require('./config');
const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

async function generateSummary(postContent) {
  const prompt = `Summarize the following blog post in 2-3 sentences:\n\n${postContent}`;
  const response = await ollama.generate({ prompt });
  return response.text;
}

async function addSummaryToPost(postPath, summary) {
  const { data, content } = matter.read(postPath);
  data.summary = summary;
  const updatedContent = matter.stringify(content, data);
  fs.writeFileSync(postPath, updatedContent);
}

async function generateSummariesForAllPosts() {
  const postsDir = path.join(__dirname, '_posts');
  const files = fs.readdirSync(postsDir);

  for (const file of files) {
    if (file.endsWith('.md')) {
      const postPath = path.join(postsDir, file);
      const { content } = matter.read(postPath);

      const summary = await generateSummary(content);
      await addSummaryToPost(postPath, summary);

      console.log(`Added AI-generated summary to ${file}`);
    }
  }
}

generateSummariesForAllPosts();
```

2. Update your GitHub Action to include summary generation:

```yaml
# .github/workflows/generate-content.yml
name: Generate AI Content, Comments, and Summaries

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight
  workflow_dispatch:  # Allow manual triggering

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - run: npm install
    - run: node generate-content.js
    - run: node generate-comments.js
    - run: node generate-summaries.js
    - name: Commit and push if changed
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
        git add -A
        git commit -m "Add AI-generated content, comments, and summaries" || exit 0
        git push
```

### Step 9: Implement Content Recommendations

To provide personalized content recommendations, you can use Ollama to analyze post content and suggest related posts:

1. Create a new file `generate-recommendations.js`:

```javascript
const ollama = require('./config');
const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

async function generateRecommendations(postContent, allPosts) {
  const prompt = `Based on the following blog post content, suggest 3 related posts from the given list of titles. Only return the titles of the recommended posts:\n\nPost content: ${postContent}\n\nAvailable posts: ${allPosts.join(', ')}`;
  const response = await ollama.generate({ prompt });
  return response.text.split('\n').map(title => title.trim());
}

async function addRecommendationsToPost(postPath, recommendations) {
  const { data, content } = matter.read(postPath);
  data.recommendations = recommendations;
  const updatedContent = matter.stringify(content, data);
  fs.writeFileSync(postPath, updatedContent);
}

async function generateRecommendationsForAllPosts() {
  const postsDir = path.join(__dirname, '_posts');
  const files = fs.readdirSync(postsDir);
  const allPostTitles = files.map(file => matter.read(path.join(postsDir, file)).data.title);

  for (const file of files) {
    if (file.endsWith('.md')) {
      const postPath = path.join(postsDir, file);
      const { content, data } = matter.read(postPath);

      const recommendations = await generateRecommendations(content, allPostTitles.filter(title => title !== data.title));
      await addRecommendationsToPost(postPath, recommendations);

      console.log(`Added AI-generated recommendations to ${file}`);
    }
  }
}

generateRecommendationsForAllPosts();
```

2. Update your GitHub Action to include recommendation generation:

```yaml
# .github/workflows/generate-content.yml
name: Generate AI Content, Comments, Summaries, and Recommendations

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight
  workflow_dispatch:  # Allow manual triggering

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Use Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '14'
    - run: npm install
    - run: node generate-content.js
    - run: node generate-comments.js
    - run: node generate-summaries.js
    - run: node generate-recommendations.js
    - name: Commit and push if changed
      run: |
        git config --global user.email "action@github.com"
        git config --global user.name "GitHub Action"
        git add -A
        git commit -m "Add AI-generated content, comments, summaries, and recommendations" || exit 0
        git push
```

### Step 10: Update Jekyll Templates

To display the new AI-generated content, you'll need to update your Jekyll templates:

1. Update your post layout (`_layouts/post.html`):

```html
---
layout: default
---
<article class="post">
  <h1>{{ page.title }}</h1>
  
  {% if page.summary %}
    <div class="summary">
      <h2>Summary</h2>
      <p>{{ page.summary }}</p>
    </div>
  {% endif %}

  <div class="post-content">
    {{ content }}
  </div>

  {% if page.recommendations %}
    <div class="recommendations">
      <h2>Recommended Posts</h2>
      <ul>
        {% for recommendation in page.recommendations %}
          <li><a href="{{ site.baseurl }}{% post_url recommendation %}">{{ recommendation }}</a></li>
        {% endfor %}
      </ul>
    </div>
  {% endif %}

  {% if page.comments %}
    <div class="comments">
      <h2>Comments</h2>
      {% for comment in page.comments %}
        <div class="comment">
          <p><strong>{{ comment.persona }}</strong>: {{ comment.content }}</p>
        </div>
      {% endfor %}
    </div>
  {% endif %}
</article>
```

### Step 11: Optimize Performance

To address potential performance issues with running AI models locally:

1. Consider using a cloud-based solution for running Ollama if your local machine struggles with performance.
2. Implement caching for AI-generated content to reduce the load on your system.
3. Use asynchronous processing to generate content in the background without affecting the blog's responsiveness.

### Step 12: Continuous Improvement

1. Regularly review and refine your AI-generated content to ensure quality and relevance.
2. Experiment with different AI models and prompts to improve the output.
3. Gather user feedback on the AI-generated content and use it to fine-tune your system.

## Conclusion

You've now set up a sophisticated Jekyll blog with Netlify CMS, Docker, and advanced AI integration using Ollama. Your blog can automatically generate new posts, provide AI-driven comments, create summaries, and offer personalized content recommendations.

This setup provides a powerful platform for creating engaging, dynamic content with minimal manual intervention. As you continue to use and refine this system, you'll be able to focus more on high-level content strategy while the AI handles much of the day-to-day content generation and engagement.

Remember to monitor the quality of AI-generated content and make adjustments as needed. The goal is to enhance your blog with AI, not to replace human creativity and insight entirely.

Happy blogging with your new AI-powered Jekyll site!