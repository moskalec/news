# from rest_framework.serializers import ModelSerializer
# from posts.models import Post, UserPostRelation, Comment
# from rest_framework import serializers


from django.contrib.auth.models import User, Group
from rest_framework import serializers

from posts.models import Post


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'image', 'url', 'category', 'tags']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']



# class CommentSerializer(ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('content', 'creation_date', 'user')
#
#
# class PostsSerializer(ModelSerializer):
#     amount_of_upvotes = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'link', 'creation_date', 'author_name', 'amount_of_upvotes')
#         # exclude = ('comments',)
#
#     def get_amount_of_upvotes(self, instance):
#         return UserPostRelation.objects.filter(post=instance, upvote=True).count()
#
#
# class PostDetailSerializer(ModelSerializer):
#     comments = CommentSerializer(source='comments.content', required=False)
#
#     class Meta:
#         model = Post
#         fields = ('id', 'title', 'link', 'creation_date', 'author_name', 'amount_of_upvotes', 'comments')
#
#
# class UserPostsRelationViewSerializer(ModelSerializer):
#     class Meta:
#         model = UserPostRelation
#         fields = ('upvote',)
