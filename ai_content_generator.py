<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import flask
from flask import Flask, request, jsonify
=======
>>>>>>> parent of 3d81fb4 (afds)
=======
>>>>>>> parent of 3d81fb4 (afds)
=======
>>>>>>> parent of 3d81fb4 (afds)
import subprocess
import sys

def generate_ai_content(prompt):
    result = subprocess.run(['ollama', 'run', 'llama3.1', prompt], capture_output=True, text=True)
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