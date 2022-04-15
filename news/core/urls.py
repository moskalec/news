from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from posts.views import PostViewSet, UserPostsRelationView, PostCommentRelationView

router = SimpleRouter()

router.register(r'post', PostViewSet)
router.register(r'post_relation', UserPostsRelationView)
router.register(r'post_comment', PostCommentRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
