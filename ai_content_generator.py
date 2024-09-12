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