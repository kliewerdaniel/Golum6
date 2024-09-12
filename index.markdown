---
layout: home
title: Daniel Kliewer
description: Exploring machine learning and web development
---

# Welcome to My Tech Blog

Hello! I'm Daniel Kliewer, a web developer with a passion for machine learning. 
This blog is where I share my thoughts, experiences, and discoveries in the world of technology.

## Recent Posts

{% for post in site.posts limit:5 %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

## About Me

I've been working in web development for over 10 years, and I'm currently exploring the exciting field of machine learning. 
Through this blog, I hope to share my journey and insights with fellow tech enthusiasts.

## Get in Touch

- Email: [danielkliewer@gmail.com](mailto:danielkliewer@gmail.com)
- GitHub: [kliewerdaniel](https://github.com/kliewerdaniel)

---

<footer>
  <p>&copy; {{ site.time | date: '%Y' }} Daniel Kliewer. All rights reserved.</p>
</footer>

<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
<script>
  if (window.netlifyIdentity) {
    window.netlifyIdentity.on("init", user => {
      if (!user) {
        window.netlifyIdentity.on("login", () => {
          document.location.href = "/admin/";
        });
      }
    });
  }
</script>