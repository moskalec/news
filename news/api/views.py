from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from api.serializers import UserSerializer, PostSerializer, TagSerializer
from posts.models import Post, Tag
from django.http import JsonResponse
from posts.models import Category
from api.serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from slugify import slugify
from django.contrib.auth import get_user_model


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)

    @action(methods=['get'], detail=True)
    def category(self, request, *args, **kwargs):
        data = Post.objects.all().values()
        serializer = PostSerializer(data=data, many=True)
        if serializer.is_valid():
            return JsonResponse(serializer.data, safe=False)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrReadOnly, IsOwnerOrReadOnly)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        if post.like.filter(username=request.user.username).exists():
            post.like.remove(request.user)
        else:
            post.like.add(request.user)
            post.dislike.remove(request.user)
        return Response({'liked': True})

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def dislike(self, request, *args, **kwargs):
        post = self.get_object()
        if post.dislike.filter(username=request.user.username).exists():
            post.dislike.remove(request.user)
        else:
            post.dislike.add(request.user)
            post.like.remove(request.user)
        return Response({'disliked': True})

    def perform_create(self, serializer):
        tags = []
        for tag in self.request.POST.dict()['tags'].split(","):
            import ipdb
            ipdb.set_trace()
            obj, _ = Tag.objects.get_or_create(title=tag.strip(), slug=slugify(tag.strip()))
            tags.append(obj)
        serializer.save(tags=tags)
        serializer.save(author_name=self.request.user)
        serializer.save(slug=slugify(self.request.POST.get('title')))
