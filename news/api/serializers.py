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
        fields = ['title', 'slug']
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


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
# class PostSerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.ReadOnlyField(source='author_name.username')
    # category = CategorySerializer()
    # tags = TagSerializer(many=True)
    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='title'
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Post
        lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }
        fields = ['slug', 'title', 'content', 'image', 'author_name', 'category', 'tags']


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.CharField(max_length=200)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags']
# class UserPostsRelationViewSerializer(ModelSerializer):
#     class Meta:
#         model = UserPostRelation
#         fields = ('upvote',)
