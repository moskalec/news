from django.contrib.auth.models import User
from rest_framework import serializers

from posts.models import Post, Category, Tag, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author_name.username')
    category = serializers.ReadOnlyField(source='category.title')

    class Meta:
        model = Post
        fields = ['slug', 'title', 'content', 'image', 'author_name', 'category']

# class UserPostsRelationViewSerializer(ModelSerializer):
#     class Meta:
#         model = UserPostRelation
#         fields = ('upvote',)
