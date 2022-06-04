from django import template
from posts.models import Post, Category

register = template.Library()


@register.inclusion_tag('core/includes/dropdown_categories.html')
def all_categories():
    categories = Category.objects.all()
    return {'categories': categories}


@register.inclusion_tag('core/includes/featured_post.html')
def featured_post():
    featured = Post.objects.order_by('-total_likes').first()
    return {'featured': featured}


@register.inclusion_tag('core/includes/latest_posts.html')
def latest_posts():
    latest = Post.latest.all()
    return {'latest': latest}
