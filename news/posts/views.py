from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostsSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]