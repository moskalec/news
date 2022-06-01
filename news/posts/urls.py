from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('posts', views.PostsListView.as_view(), name='post-list'),
    path('category/', views.CategoriesListView.as_view(), name='category-list'),
    path('tag/', views.TagDetailView.as_view(), name='tags-list'),
    path('tag/<slug:tag_slug>/', views.TagsListView.as_view(), name='tag-detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('mine/', views.ManagePostListView.as_view(), name='manage_post_list'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
