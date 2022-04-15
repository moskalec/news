from django.contrib import admin

from posts.models import Post, UserPostRelation, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPostRelation)
class UserPostRelation(admin.ModelAdmin):
    pass
