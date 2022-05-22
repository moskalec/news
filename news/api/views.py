# from rest_framework.viewsets import ModelViewSet
# from posts.models import Post, UserPostRelation, Comment
# from api.serializers import PostsSerializer, UserPostsRelationViewSerializer, CommentSerializer, PostDetailSerializer
# from rest_framework.mixins import UpdateModelMixin
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from api.serializers import UserSerializer, PostSerializer, CommentSerializer, TagSerializer
from posts.models import Post, Comment, Tag
#########
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from posts.models import Category
from api.serializers import CategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from slugify import slugify


#########

# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('api:user-list', request=request, format=format),
#         'posts': reverse('api:post-list', request=request, format=format),
#         'categories': reverse('api:category-list', request=request, format=format),
#     })


# class CommentList(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
#
# class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


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
        # data = Post.objects.filter(category__slug=self.kwargs.get('slug'))#.values()
        data = Post.objects.all().values()
        serializer = PostSerializer(data=data, many=True)
        if serializer.is_valid():
            return JsonResponse(serializer.data, safe=False)
            # return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
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

#################
# class PostsViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all().order_by('-created')
#     serializer_class = PostsSerializer


# permission_classes = [permissions.IsAuthenticated]
# lookup_field = 'username'
# view_name = 'api:user-list'

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class PostViewSet(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostsSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.validated_data['author_name'] = self.request.user
#         serializer.save()
#
#
# class PostView(ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.validated_data['author_name'] = self.request.user
#         serializer.save()
#
#
# class PostCommentRelationView(UpdateModelMixin, GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     lookup_field = 'post'
#
#     def get_object(self):
#         obj, _ = Comment.objects.get_or_create(user=self.request.user, post_id=self.kwargs['post'])
#         return obj
#
#
# class UserPostsRelationView(UpdateModelMixin, GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = UserPostRelation.objects.all()
#     serializer_class = UserPostsRelationViewSerializer
#     lookup_field = 'post'
#
#     def get_object(self):
#         obj, _ = UserPostRelation.objects.get_or_create(user=self.request.user, post_id=self.kwargs['post'])
#         return obj
