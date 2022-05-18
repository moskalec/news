from django.contrib import admin
from django.urls import path, include
# from rest_framework.routers import SimpleRouter

# from api.views import PostViewSet, UserPostsRelationView, PostCommentRelationView, PostView
from django.conf import settings
from django.conf.urls.static import static

# router = SimpleRouter()

# router.register(r'post', PostViewSet)
# router.register(r'post-detail', PostView)
# router.register(r'post_relation', UserPostsRelationView)
# router.register(r'post_comment', PostCommentRelationView)

# app_name = 'news'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('', include('posts.urls', namespace='posts')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
]

# urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
