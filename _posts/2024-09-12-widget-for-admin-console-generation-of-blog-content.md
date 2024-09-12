---
layout: post
title: Widget for Admin Console Generation of Blog Content
date: 2024-09-12T17:18:50.172Z
---

## Widget for Admin Console Generation of Blog Content

### Step 1: Create the AI Content Widget

1. Create a new file: `admin/ai-content-widget.js`:

```js
const AIContentWidget = createClass({
  handleGenerate: function() {
    const title = this.props.value.get('title') || '';
    fetch('/generate-ai-content', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ title }),
    })
    .then(response => response.json())
    .then(data => {
      this.props.onChange({
        title: title,
        body: data.content,
        ai_comments: data.comments,
      });
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  },

  render: function() {
    const {forID, classNameWrapper, value, onChange} = this.props;
    return h('div', {className: classNameWrapper},
      h('input', {
        type: 'text',
        id: forID,
        className: classNameWrapper,
        value: value ? value.get('title') : '',
        onChange: e => onChange({title: e.target.value}),
      }),
      h('button', {
        className: 'btn',
        onClick: this.handleGenerate
      }, 'Generate AI Content')
    );
  }
});

CMS.registerWidget('ai-content', AIContentWidget);
```

### Step 2: Modify the Admin Panel

1. Update `admin/index.html` to include the new widget:

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
  <script src="ai-content-widget.js"></script>
</body>
</html>
```

### Step 3: Update `config.yml` for the New Widget

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
      - {label: "AI Content", name: "ai_content", widget: "ai-content"}
      - {label: "Body", name: "body", widget: "markdown"}
      - {label: "AI Comments", name: "ai_comments", widget: "text"}
```

### Step 4: Set up the AI Content API

1. Modify `ai_content_generator.py` to serve as an API endpoint:

```python
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def generate_ai_content(prompt):
    result = subprocess.run(['ollama', 'run', 'llama2', prompt], capture_output=True, text=True)
    return result.stdout

def generate_blog_post(title):
    prompt = f"Write a short blog post with the title: {title}"
    return generate_ai_content(prompt)

def generate_comments(post_content):
    prompt = f"Generate 3 short, diverse comments for the following blog post:\n\n{post_content}"
    return generate_ai_content(prompt)

@app.route('/generate-ai-content', methods=['POST'])
def generate_content():
    data = request.json
    title = data.get('title', '')

    post_content = generate_blog_post(title)
    comments = generate_comments(post_content)

    return jsonify({
        'content': post_content,
        'comments': comments
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

### Step 5: Configure Netlify for the Flask API

1. Create a `netlify.toml` file in the root of your project:

```toml
[build]
  command = "jekyll build"
  publish = "_site"

[[redirects]]
  from = "/generate-ai-content"
  to = "http://localhost:5000/generate-ai-content"
  status = 200
  force = true

[dev]
  command = "jekyll serve"
```

### Step 6: Install `jekyll-admin` Gem

1. Update your `Gemfile`:

```ruby
gem "jekyll-admin", group: :jekyll_plugins
```

2. Run `bundle install`.

### Step 7: Create an AI Content Formatter Plugin

1. Create `_plugins/ai_content_formatter.rb`:

```ruby
module Jekyll
  class AIContentFormatter
    def self.format(site, page)
      return unless page['ai_content']

      title = page['ai_content']['title']
      content = page['ai_content']['body']
      comments = page['ai_content']['ai_comments']

      formatted_content = <<~CONTENT
        ---
        layout: post
        title: "#{title}"
        date: #{Time.now.strftime('%Y-%m-%d %H:%M:%S %z')}
        categories: []
        ---

        #{content}

        ## AI-Generated Comments
        #{comments}
      CONTENT

      page.content = formatted_content
    end
  end

  class AIContentGenerator < Generator
    def generate(site)
      site.pages.each do |page|
        AIContentFormatter.format(site, page)
      end
    end
  end
end
```

### Step 8: Update `_config.yml`

```yaml
plugins:
  - jekyll-admin
  - jekyll/ai_content_formatter
```

---

### Usage Instructions:

1. **Start the Jekyll server:**

    ```bash
    bundle exec jekyll serve
    ```

2. **In another terminal, start the Flask app:**

    ```bash
    python ai_content_generator.py
    ```

3. **Access the admin panel:**

    - Go to `http://localhost:4000/admin/`.

4. **Create a new blog post:**

    - Enter a title.
    - Click "Generate AI Content" to fill in the body and comments.

5. **Publish the post:**

    - The AI-generated content will be saved as a `.md` file in the `_posts` folder.

---

### Additional Steps:

1. **Install required Python packages:**

    ```bash
    pip install flask
    ```

2. **Update `.gitignore` file:**

    ```bash
    *.pyc
    __pycache__/
    .env
    ```

3. **Create a `requirements.txt` file:**

    ```txt
    Flask==2.0.1
    ```

4. **Add Python runtime to `netlify.toml`:**

    ```toml
    [build.environment]
      PYTHON_VERSION = "3.8"
    ```

5. **Create a `runtime.txt` file:**

    ```txt
    python-3.8.12
    ```

---

### Best Practices:

- **Security:** Use environment variables for sensitive data.
- **Caching:** Implement caching for AI-generated content.
- **Customization:** Adjust AI prompts to fit your blog's tone.
- **Testing:** Create unit tests for the Python script and Jekyll plugin.

This setup gives you the ability to generate AI-enhanced content directly from your admin panel, while maintaining Jekyll's flexibility.