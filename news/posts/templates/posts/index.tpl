{% extends 'core/base.html' %}

{% block content %}
Tags:
{% for tag in tags %}
    <a href="{{ tag.get_absolute_url }}">{{ tag }}</a>
{% endfor %}
<br>
featured post: <a href="{{ featured_post.get_absolute_url }}">{{ featured_post.title }}</a>
<br>
latest_posts:
<ul>
    {% for post in latest_posts %}
    <li><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></li>
    {% endfor %}
</ul>
<br>
All posts: <a href="{% url 'posts:post-list' %}">posts</a>

{% endblock %}
