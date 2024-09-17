import os
import random
import requests
import frontmatter
from personas import PERSONAS

def generate_comment(post_content, persona):
    url = "http://localhost:11434/api/generate"
    prompt = f"As a {persona['name']} ({persona['description']}), comment on this post:\n\n{post_content}"
    data = { "model": "llama3.1", "prompt": prompt, "stream": False }
    response = requests.post(url, json=data)
    return response.json()["response"]

def generate_comments_for_post(post_content, num_comments=3):
    if not post_content.strip():
        raise ValueError("Post content is empty")
    selected_personas = random.sample(PERSONAS, num_comments)
    return [{ "persona": p['name'], "comment": generate_comment(post_content, p) } for p in selected_personas]

def get_posts(posts_dir):
    posts = []
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            posts.append(filename)
    return posts

def select_post(posts):
    print("Available posts:")
    for i, post in enumerate(posts):
        print(f"{i + 1}. {post}")
    selection = int(input("Enter the number of the post you want to generate comments for: ")) - 1
    return posts[selection]

def append_comments_to_post(post_path, comments):
    with open(post_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find the end of the frontmatter
    frontmatter_end = content.find('---', content.find('---') + 3) + 3
    
    # Split the content into frontmatter and body
    frontmatter = content[:frontmatter_end]
    body = content[frontmatter_end:].strip()
    
    # Append comments
    comments_section = "\n\n## Comments\n"
    for comment in comments:
        comments_section += f"\n### {comment['persona']}\n{comment['comment']}\n"
    
    # Combine everything
    new_content = frontmatter + '\n' + body + comments_section
    
    # Write the new content back to the file
    with open(post_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def main():
    posts_dir = '_posts'  # Update this to your Jekyll posts directory
    try:
        posts = get_posts(posts_dir)
        if not posts:
            print(f"No .md files found in {posts_dir}")
            return
        
        selected_post = select_post(posts)
        
        post_path = os.path.join(posts_dir, selected_post)
        print(f"Reading file: {post_path}")
        
        with open(post_path, 'r', encoding='utf-8') as file:
            raw_content = file.read()
            print(f"Raw file content (first 500 characters):\n{raw_content[:500]}")
        
        post = frontmatter.loads(raw_content)
        
        if not post.content.strip():
            print(f"The content of '{selected_post}' is empty after parsing frontmatter.")
            print("Frontmatter:", post.metadata)
            return
        
        print(f"Post content (first 500 characters):\n{post.content[:500]}")
        
        comments = generate_comments_for_post(post.content)
        print("Generated comments:")
        for comment in comments:
            print(f"{comment['persona']}: {comment['comment'][:100]}...")  # Print first 100 chars of each comment
        
        append_comments_to_post(post_path, comments)
        
        print(f"Comments have been added to {selected_post}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()