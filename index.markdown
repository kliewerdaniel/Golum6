---
layout: home
title: Daniel Kliewer
description: Exploring machine learning and web development
---


## Recent Posts

{% for post in site.posts limit:5 %}
- [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}


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