---
layout: home
title: Improved Article From Comments
date: 2024-09-17T17:02:33.026Z
---
This guide provides a step-by-step setup for your enhanced Jekyll blog with features such as SEO, performance improvements, and various integrations.


## Script for `golum.sh`


```bash
#!/bin/bash


# Jekyll Blog Setup Script with Enhancements


set -e
echo "Setting up your enhanced Jekyll blog with headless CMS, Docker, and Netlify..."


# Existing steps: Step 1-5


# Step 6: Add SEO Optimization
echo "gem 'jekyll-seo-tag'" >> Gemfile
echo "gem 'jekyll-sitemap'" >> Gemfile
sed -i "s/plugins:/plugins:\n  - jekyll-seo-tag\n  - jekyll-sitemap/" _config.yml


# Step 7: Add Performance Improvements
echo "gem 'jekyll-minifier'" >> Gemfile
sed -i "s/plugins:/plugins:\n  - jekyll-minifier/" _config.yml
```


## Content Features


Create a new file for post meta:


```html
<span class="post-meta">
 
</span>
```


Create the `reading-time.html`:


```html

```


## Layout Enhancements


### Custom 404 Page


```html
---
layout: default
title: 404 - Page Not Found
permalink: /404.html
---


<h1>404 - Page Not Found</h1>
<p>Sorry, the page you're looking for doesn't exist. Try going back to the <a href="/">homepage</a>.</p>
```


### RSS Feed Integration


Add this to the Gemfile:


```bash
echo "gem 'jekyll-feed'" >> Gemfile
sed -i "s/plugins:/plugins:\n  - jekyll-feed/" _config.yml
```


### SEO & Social Media Settings


Add the following to your `_config.yml`:


```yml
title: My Enhanced Jekyll Blog
description: A feature-rich Jekyll blog with Netlify CMS and Docker
author: Your Name
url: "https://your-site-url.com"


# Social media
twitter_username: yourusername
github_username: yourusername


# Pagination
paginate: 5
paginate_path: "/page:num/"
```


### Adding Google Analytics


Create the include file:


```html
<script async src="https://www.googletagmanager.com/gtag/js?id={{ "{{ site.google_analytics }}" }}"></script>
<script>
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', '{{ "{{ site.google_analytics }}" }}');
</script>
```


And add it to the layout:


```html

```


### Syntax Highlighting with Rouge


```bash
echo "gem 'rouge'" >> Gemfile
sed -i "s/plugins:/plugins:\n  - rouge/" _config.yml
echo "highlighter: rouge" >> _config.yml
```


## Final Customization


### Adding `robots.txt`


```text
User-agent: *
Allow: /
Sitemap: {{ "{{ site.url }}" }}/sitemap.xml
```


### Customizing `about.md`


```md
---
layout: page
title: About
permalink: /about/
---


This is an enhanced Jekyll blog with various features including SEO optimization, performance improvements, and more.
```


### Enabling Dark Mode


Add the script:


```js
const darkModeToggle = document.getElementById('dark-mode-toggle');
const body = document.body;


darkModeToggle.addEventListener('click', () => {
 body.classList.toggle('dark-mode');
 localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
});


if (localStorage.getItem('darkMode') === 'true') {
 body.classList.add('dark-mode');
}
```


Update the layout:


```html
<button id="dark-mode-toggle">Toggle Dark Mode</button>
<script src="{{ "{{ '/assets/js/dark-mode-toggle.js' | relative_url }}" }}"></script>
```


### Optimizing Images


```bash
#!/bin/bash
find . -name "*.png" -exec pngquant --force --ext .png {} +
find . -name "*.jpg" -exec jpegoptim --strip-all {} +
echo "Image optimization complete!"
```


### Structured Data for Blog Posts


```html

```


Feel free to adjust any sections as needed to match your preferences. This script provides significant enhancements to improve performance, accessibility, and features for your Jekyll blog.
