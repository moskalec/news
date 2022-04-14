from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostsSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer