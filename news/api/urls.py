from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostsViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]