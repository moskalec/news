from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.urls import reverse

from core.models import BaseModel

from pytils.translit import slugify


class PublicationBaseModel(BaseModel):
    title = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name=_('Title')
    )
    slug = models.SlugField(
        max_length=200,
        blank=True,
        unique=True,
        verbose_name=_('Slug')
    )

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Tag(PublicationBaseModel):

    def get_absolute_url(self):
        return reverse('posts:tag-detail', kwargs={'tag_slug': self.slug})

    class Meta:
        ordering = ('-title',)


class Category(PublicationBaseModel):
    description = models.TextField(
        blank=True
    )

    def get_absolute_url(self):
        return reverse('posts:category-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-title',)


# class FeaturedPostManager(models.Manager):
#     def get_queryset(self):
#         return super(FeaturedPostManager, self).get_queryset().order_by('-total_likes').first()


class LatestPostManager(models.Manager):
    def get_queryset(self):
        return super(LatestPostManager, self).get_queryset().order_by('-created')[:5]


class Post(PublicationBaseModel):
    content = models.TextField(
        verbose_name=_('Content'),
        blank=True
    )
    image = models.ImageField(
        upload_to='images/%Y/%m/%d/',
        null=True,
        blank=True
    )
    # url = models.URLField(
    #     blank=True,
    #     null=True
    # )
    category = models.ForeignKey(
        Category,
        related_name='category_posts',
        null=True,
        on_delete=models.DO_NOTHING
    )
    author_name = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True
    )
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='posts_liked',
        blank=True
    )
    dislike = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='posts_disliked',
        blank=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags'
    )
    objects = models.Manager()
    # featured = FeaturedPostManager()
    latest = LatestPostManager()
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0
    )

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)


class Comment(BaseModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    author_name = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='comments',
        on_delete=models.SET_NULL,
        null=True
    )
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.DO_NOTHING
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comments_liked',
        blank=True
    )
    dislike = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comments_disliked',
        blank=True
    )

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.author_name} on {self.post}'
