from django.contrib import admin

from posts.models import Post, UserPostRelation, Comment, Category, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'updated', 'author_name', 'content']
    list_filter = ['title', 'created', 'updated']
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'content')


@admin.register(UserPostRelation)
class UserPostRelation(admin.ModelAdmin):
    pass
