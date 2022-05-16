from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.urls import reverse


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=150, unique=True, blank=True, verbose_name=_('Slug'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post-list', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name=_('Title'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post-list', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Content'), blank=True)
    slug = models.CharField(max_length=150, unique=True, blank=True, verbose_name=_('Slug'))
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True,
                                   verbose_name=_('Created at'))
    updated = models.DateTimeField(null=True, blank=True, verbose_name=_('Updated at'))
    category = models.ForeignKey(Category,
                                 related_name='category_posts',
                                 null=True,
                                 on_delete=models.DO_NOTHING)
    author_name = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                  related_name='posts_liked',
                                  blank=True)
    dislike = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='posts_disliked',
                                     blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags')

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name='comments')

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.DO_NOTHING)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='comments_liked',
                                        blank=True)
    dislike = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='comments_disliked',
                                     blank=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'


class UserPostRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    upvote = models.BooleanField(default=False)
