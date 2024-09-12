---
layout: post
title: Jekyll Blog Setup with Netlify CMS and Docker
date: 2024-09-11T23:51:46.803Z
---

# Jekyll Blog Setup with Netlify CMS and Docker

This guide provides instructions for setting up a Jekyll blog with Netlify CMS, Docker, and Netlify deployment.

## Prerequisites

Ensure you have the following installed:

1. Git
2. Docker and Docker Compose
3. Ruby (version 3.0.0 or later)
4. Bundler
5. Jekyll
6. Node.js and npm
7. Netlify CLI

Install these on Unix-based systems (Linux, macOS) using:

# Install Git

sudo apt-get update

sudo apt-get install git

# Install Docker and Docker Compose

Follow the official Docker documentation for your specific OS

# Install Ruby (using rbenv)

sudo apt-get install rbenv

rbenv install 3.0.0

rbenv global 3.0.0

# Install Bundler and Jekyll

gem install bundler jekyll

# Install Node.js and npm

sudo apt-get install nodejs npm

# Install Netlify CLI

npm install netlify-cli -g

# Getting Started

# Clone the repository:

git clone https://github.com/kliewerdaniel/golum2.git

In it is golum.sh, the .sh file I created to set up the blog:

```bash
#!/bin/bash

# Jekyll Blog Setup Script

set -e

echo "Setting up your Jekyll blog with headless CMS, Docker, and Netlify..."

# Step 1: Create a new Jekyll site
echo "Creating new Jekyll site..."
jekyll new golum3
cd golum3

# Step 2: Set up Git repository
echo "Initializing Git repository..."
git init
git add .
git commit -m "Initial commit"

# Step 3: Create Dockerfile
echo "Creating Dockerfile..."
cat << EOF > Dockerfile
FROM jekyll/jekyll:4.2.0
WORKDIR /srv/jekyll
COPY . .
RUN bundle install
CMD ["jekyll", "serve", "--force_polling", "-H", "0.0.0.0"]
EOF

# Step 4: Create docker-compose.yml
echo "Creating docker-compose.yml..."
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
echo "Setting up Netlify CMS..."
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

# Step 6: Create .ruby-version file
echo "Creating .ruby-version file..."
echo "3.0.0" > .ruby-version

# Step 8: Build and run Docker container
echo "Building and running Docker container..."
docker-compose up -d

# Step 9: Netlify setup
echo "Setting up Netlify..."
netlify init

# Step 10: Push to GitHub (assumes you've created a repo)
echo "Please enter your GitHub repository URL:"
read repo_url
git remote add origin $repo_url
git push -u origin main

echo "Setup complete! Your blog is now running locally and set up for Netlify deployment."
echo "Next steps:"
echo "1. Visit http://localhost:4000 to view your blog locally."
echo "2. Use the Netlify CMS at http://localhost:4000/admin to manage content."
echo "3. Edit files directly in your preferred code editor."
echo "4. Commit and push changes to trigger Netlify deployment."
'''

cd golum3

# Make the setup script executable:

chmod +x golum.sh

# Run the setup script:

./golum.sh

# Follow the prompts in the script. It will:

Create a new Jekyll site

Set up Git

Create a Dockerfile and docker-compose.yml

Set up Netlify CMS

Build and run the Docker container

Initialize Netlify

Push to GitHub (you'll need to provide your GitHub repository URL)


After the script completes, your blog will be running locally and set up for Netlify deployment.

# Next Steps

Visit http://localhost:4000 to view your blog locally.

Use the Netlify CMS at http://localhost:4000/admin to manage content.

Edit files directly in your preferred code editor.

Commit and push changes to trigger Netlify deployment.

# Customization

Modify _config.yml to change your blog's settings.

Edit or add templates in the _layouts and _includes directories.

Customize styles in the assets/css directory.

# Troubleshooting

If you encounter issues:

Ensure all prerequisites are correctly installed.

Check that your local Ruby version matches the one specified in .ruby-version (3.0.0).

Verify that the Bundler version in Gemfile.lock is compatible with Ruby 3.0.0.

# Folder Structure

After running the setup script, your project structure should look like this:

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

# Using Docker

Useful Docker commands:

Start the container: docker-compose up -d

Stop the container: docker-compose down

View logs: docker-compose logs -f

Rebuild the container after changes: docker-compose up -d --build

# Writing Blog Posts

1. Using Netlify CMS:

Navigate to http://localhost:4000/admin

Log in and use the interface to create or edit posts

2. Manually:
   - Create a new file in the `_posts` directory
   - Name it `YYYY-MM-DD-title.md`
   - Add front matter at the top of the file:
     ```yaml
     ---
     layout: post
     title: "Your Post Title"
     date: YYYY-MM-DD HH:MM:SS +/-TTTT
     categories: [category1, category2]
     ---
     ```
   - Write your post content in Markdown below the front matter

## Deployment

This setup uses Netlify for deployment:

1. Push changes to your GitHub repository
2. Netlify automatically detects the push and starts a new build
3. Once the build is complete, Netlify deploys your site

To view your deployment settings or trigger a manual deploy:

1. Log in to your Netlify account
2. Select your site
3. Go to the "Deploys" tab

## SEO Optimization

To improve your blog's SEO:

1. Edit `_config.yml` and fill in the `title`, `description`, and `author` fields
2. Consider installing the `jekyll-seo-tag` plugin
3. Use descriptive titles and fill out front matter for each post
4. Use headings (H1, H2, etc.) appropriately in your content

## Performance Optimization

To ensure your blog loads quickly:

1. Optimize images before uploading
2. Minimize use of external scripts and stylesheets
3. Consider using a CDN for assets
4. Enable Netlify's asset optimization features in your Netlify dashboard

## Backing Up Your Blog

While Git serves as a form of backup, consider these additional steps:

1. Regularly push changes to GitHub
2. Set up a secondary remote repository as a backup
3. Periodically download a local copy of your entire repository

## Getting Help

If you encounter any issues or have questions:

1. Check the [Jekyll documentation](https://jekyllrb.com/docs/)
2. Visit the [Netlify CMS community forum](https://community.netlify.com/c/netlify-cms/13)
3. Search for similar issues on Stack Overflow
4. Open an issue in this GitHub repository

Remember, the Jekyll and web development communities are generally friendly and helpful. Don't hesitate to ask for help when you need it!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

---

By following this guide, you should have a fully functional Jekyll blog set up with Netlify CMS, Docker, and Netlify deployment. Happy blogging!