from django import template
from django.conf import settings

from posts.models import Post, Category

import redis

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
)
register = template.Library()


@register.inclusion_tag('core/includes/dropdown_categories.html')
def all_categories():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('core/includes/featured_post.html')
def featured_post():
    featured = Post.objects.order_by('-total_likes').first()
    return {'featured': featured}


@register.inclusion_tag('core/includes/most_viewed_post.html')
def most_viewed_post():
    post_ranking_id = r.zrevrange('post_ranking', 0, 0)
    most_viewed = Post.objects.get(id=int(post_ranking_id.pop()))

    return {'most_viewed': most_viewed}


@register.inclusion_tag('core/includes/latest_posts.html')
def latest_posts():
    latest = Post.latest.all()
    return {'latest': latest}
