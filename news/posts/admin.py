from django.contrib import admin

from posts.models import Post, Comment, Category, Tag

admin.site.index_template = 'memcache_status/admin_index.html'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated', 'author_name', 'active']
    list_filter = ['title', 'created']
    search_fields = ['title', ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'active']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'active']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'content')
