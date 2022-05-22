from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename="posts")
router.register(r'users', views.UserViewSet, basename="users")
router.register(r'categories', views.CategoryViewSet, basename="categories")
router.register(r'tags', views.TagViewSet, basename="tags")

app_name = 'api'

urlpatterns = [
    path('', include((router.urls, 'api'), namespace='api')),
]
