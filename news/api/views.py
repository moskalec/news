from rest_framework.viewsets import ModelViewSet
from posts.models import Post, UserPostRelation, Comment
from api.serializers import PostsSerializer, UserPostsRelationViewSerializer, CommentSerializer, PostDetailSerializer
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author_name'] = self.request.user
        serializer.save()


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.validated_data['author_name'] = self.request.user
        serializer.save()


class PostCommentRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'post'

    def get_object(self):
        obj, _ = Comment.objects.get_or_create(user=self.request.user, post_id=self.kwargs['post'])
        return obj


class UserPostsRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserPostRelation.objects.all()
    serializer_class = UserPostsRelationViewSerializer
    lookup_field = 'post'

    def get_object(self):
        obj, _ = UserPostRelation.objects.get_or_create(user=self.request.user, post_id=self.kwargs['post'])
        return obj
