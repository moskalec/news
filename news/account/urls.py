from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import UserDetailView, UserListView

app_name = 'account'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<slug:slug>/follow/', UserDetailView.as_view(), name='user_follow'),
    path('users/<slug:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('edit/', views.UserProfileEditView.as_view(), name='edit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
