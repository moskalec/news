from django.urls import path

from .views import PostsListView, PostDetailView, HomePageView, CategoriesListView
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'posts'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('like/', views.like_dislike, name='like_dislike'),
    path('posts', PostsListView.as_view(), name='post-list'),
    path('category/', CategoriesListView.as_view(), name='category-list'),
    path('create/', views.post_create, name='create'),
    path('tag/<slug:tag_slug>/', PostsListView.as_view(), name='post-list'),
    path('category/<slug:category_slug>/', PostsListView.as_view(), name='post-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
