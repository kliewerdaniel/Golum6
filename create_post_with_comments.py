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