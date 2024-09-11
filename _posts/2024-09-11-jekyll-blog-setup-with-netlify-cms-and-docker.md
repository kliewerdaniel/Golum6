---
layout: post
title: Jekyll Blog Setup with Netlify CMS and Docker
date: 2024-09-11T23:51:46.803Z
---
\# Jekyll Blog Setup with Netlify CMS and Docker



This repository contains a script and instructions for setting up a Jekyll blog with Netlify CMS, Docker, and Netlify deployment.



\## Prerequisites



Before you begin, ensure you have the following installed on your system:



1. Git

2. Docker and Docker Compose

3. Ruby (version 3.0.0 or later)

4. Bundler

5. Jekyll

6. Node.js and npm

7. Netlify CLI



You can install these on most Unix-based systems (Linux, macOS) using the following commands:



\`\``bash

\# Install Git

sudo apt-get update

sudo apt-get install git



\# Install Docker and Docker Compose

\# Follow the official Docker documentation for your specific OS



\# Install Ruby (using rbenv)

sudo apt-get install rbenv

rbenv install 3.0.0

rbenv global 3.0.0



\# Install Bundler and Jekyll

gem install bundler jekyll



\# Install Node.js and npm

sudo apt-get install nodejs npm



\# Install Netlify CLI

npm install netlify-cli -g

## Getting Started

Clone this repository:\
Copy\
git clone https://github.com/kliewerdaniel/golum2.git

1. cd golum3
2. Make the setup script executable:\
   Copy\
   chmod +x golum.sh
3. Run the setup script:\
   Copy\
   ./golum.sh
4. Follow the prompts in the script. It will:
5. * Create a new Jekyll site
   * Set up Git
   * Create a Dockerfile and docker-compose.yml
   * Set up Netlify CMS
   * Build and run the Docker container
   * Initialize Netlify
   * Push to GitHub (you'll need to provide your GitHub repository URL)
6. After the script completes, your blog will be running locally and set up for Netlify deployment.

## Next Steps

1. Visit http://localhost:4000 to view your blog locally.
2. Use the Netlify CMS at http://localhost:4000/admin to manage content.
3. Edit files directly in your preferred code editor.
4. Commit and push changes to trigger Netlify deployment.

## Customization

* Modify _config.yml in your new blog directory to change your blog's settings.
* Edit or add templates in the _layouts and _includes directories.
* Customize styles in the assets/css directory.

## Troubleshooting

If you encounter any issues:

* Ensure all prerequisites are correctly installed.
* Check that your local Ruby version matches the one specified in .ruby-version (3.0.0).
* Verify that the Bundler version in Gemfile.lock is compatible with Ruby 3.0.0.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.



\## Folder Structure



After running the setup script, your project structure should look like this:

my-blog/ ├── _posts/ ├── _site/ ├── admin/ │ ├── config.yml │ └── index.html ├── assets/ │ └── uploads/ ├── _config.yml ├── Dockerfile ├── docker-compose.yml ├── Gemfile ├── Gemfile.lock └── .ruby-version



\## Using Docker



The setup script creates a Dockerfile and docker-compose.yml file for you. Here are some useful Docker commands:



\- Start the container: \`docker-compose up -d\`

\- Stop the container: \`docker-compose down\`

\- View logs: \`docker-compose logs -f\`

\- Rebuild the container after changes: \`docker-compose up -d --build\`



\## Writing Blog Posts



1. Using Netlify CMS:

\- Navigate to \`http://localhost:4000/admin\`

\- Log in and use the interface to create or edit posts



2. Manually:

\- Create a new file in the \`_posts\` directory

\- Name it \`YYYY-MM-DD-title.md\`

\- Add front matter at the top of the file:

     \`\``yaml

\---

     layout: post

     title: "Your Post Title"

     date: YYYY-MM-DD HH:MM:SS +/-TTTT

     categories: \[category1, category2]

\---

     \`\``

\- Write your post content in Markdown below the front matter



\## Deployment



This setup uses Netlify for deployment. Here's how it works:



1. Push changes to your GitHub repository

2. Netlify automatically detects the push and starts a new build

3. Once the build is complete, Netlify deploys your site



To view your deployment settings or trigger a manual deploy:



1. Log in to your Netlify account

2. Select your site

3. Go to the "Deploys" tab



\## SEO Optimization



To improve your blog's SEO:



1. Edit \`_config.yml\` and fill in the \`title\`, \`description\`, and \`author\` fields

2. Consider installing the \`jekyll-seo-tag\` plugin

3. Use descriptive titles and fill out front matter for each post

4. Use headings (H1, H2, etc.) appropriately in your content



\## Performance Optimization



To ensure your blog loads quickly:



1. Optimize images before uploading

2. Minimize use of external scripts and stylesheets

3. Consider using a CDN for assets

4. Enable Netlify's asset optimization features in your Netlify dashboard



\## Backing Up Your Blog



While Git serves as a form of backup, consider these additional steps:



1. Regularly push changes to GitHub

2. Set up a secondary remote repository as a backup

3. Periodically download a local copy of your entire repository



\## Getting Help



If you encounter any issues or have questions:



1. Check the \[Jekyll documentation](https://jekyllrb.com/docs/)

2. Visit the \[Netlify CMS community forum](https://community.netlify.com/c/netlify-cms/13)

3. Search for similar issues on Stack Overflow

4. Open an issue in this GitHub repository



Remember, the Jekyll and web development communities are generally friendly and helpful. Don't hesitate to ask for help when you need it!