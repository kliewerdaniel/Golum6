---
layout: home
title: Jekyll Blog Setup with Netlify CMS and Docker
date: 2024-09-11T23:51:46.803Z
---

# Jekyll Blog Setup with Netlify CMS and Docker

This guide provides step-by-step instructions to set up a Jekyll blog using Netlify CMS, Docker, and Netlify for deployment.

---

## Prerequisites

Make sure you have the following installed on your system:

- **Git**
- **Docker** and **Docker Compose**
- **Ruby** (version 3.0.0 or later)
- **Bundler**
- **Jekyll**
- **Node.js** and **npm**
- **Netlify CLI**

### Install Git
```bash
sudo apt-get update
sudo apt-get install git
```

### Install Docker and Docker Compose
Follow the official Docker documentation for your OS.

### Install Ruby using `rbenv`
```bash
sudo apt-get install rbenv
rbenv install 3.0.0
rbenv global 3.0.0
```

### Install Bundler and Jekyll
```bash
gem install bundler jekyll
```

### Install Node.js and npm
```bash
sudo apt-get install nodejs npm
```

### Install Netlify CLI
```bash
npm install netlify-cli -g
```

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/kliewerdaniel/golum2.git
```

The repository contains `golum.sh`, a script to set up the blog.

### Beginning of `golum.sh`:

```bash
#!/bin/bash

# Jekyll Blog Setup Script

set -e
echo "Setting up your Jekyll blog with headless CMS, Docker, and Netlify..."

# Step 1: Create a new Jekyll site
jekyll new golum3
cd golum3

# Step 2: Set up Git repository
git init
git add .
git commit -m "Initial commit"

# Step 3: Create Dockerfile
cat << EOF > Dockerfile
FROM jekyll/jekyll:4.2.0
WORKDIR /srv/jekyll
COPY . .
RUN bundle install
CMD ["jekyll", "serve", "--force_polling", "-H", "0.0.0.0"]
EOF

# Step 4: Create docker-compose.yml
cat << EOF > docker-compose.yml
version: '3'
services:
  site:
    command: jekyll serve --force_polling
    image: jekyll/jekyll:4.2.0
    volumes:
      - .:/srv/jekyll
    ports:
      - 4000:4000
EOF

# Step 5: Set up Netlify CMS
mkdir -p admin
cat << EOF > admin/config.yml
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
      - {label: "Body", name: "body", widget: "markdown"}
EOF

cat << EOF > admin/index.html
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Content Manager</title>
</head>
<body>
  <script src="https://unpkg.com/netlify-cms@^2.0.0/dist/netlify-cms.js"></script>
</body>
</html>
EOF
```

---

## Running the Setup Script

After cloning the repository, navigate to the directory and make the script executable:

```bash
cd golum3
chmod +x golum.sh
./golum.sh
```

### The Script Will:

1. Create a new Jekyll site
2. Set up Git
3. Create a Dockerfile and docker-compose.yml
4. Set up Netlify CMS
5. Build and run the Docker container
6. Initialize Netlify
7. Push your code to GitHub

---

## Next Steps

Once the setup is complete, you can:

- Visit `http://localhost:4000` to view your blog locally.
- Use the Netlify CMS at `http://localhost:4000/admin` to manage content.
- Commit and push changes to GitHub to trigger deployment on Netlify.

### Project Structure After Setup

```bash
my-blog/
├── _posts/
├── _site/
├── admin/
│   ├── config.yml
│   └── index.html
├── assets/
│   └── uploads/
├── _config.yml
├── Dockerfile
├── docker-compose.yml
├── Gemfile
├── Gemfile.lock
└── .ruby-version
```

---

## Customization

- Modify `_config.yml` for basic settings.
- Edit or add templates in the `_layouts` and `_includes` directories.
- Customize styles in the `assets/css` directory.

---

## Troubleshooting

- Ensure all prerequisites are correctly installed.
- Confirm the local Ruby version matches `.ruby-version` (3.0.0).
- Verify the Bundler version is compatible with Ruby 3.0.0.

---

## Deployment

1. Push changes to your GitHub repository.
2. Netlify will automatically detect changes and trigger a new build.
3. Once the build is complete, Netlify will deploy your site.

---

## Writing Blog Posts

You can create blog posts using the Netlify CMS or manually in the `_posts` directory.

### Manual Post Example

```yaml
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [category1, category2]
---
Your post content in Markdown goes here.
```

---

## Conclusion

By following this guide, you’ll have a fully functional Jekyll blog integrated with Netlify CMS, Docker, and Netlify deployment.

For additional resources:

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Netlify CMS Documentation](https://www.netlifycms.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
```

This formatting will improve the structure and readability when rendered on your website, making it easier for users to follow along.