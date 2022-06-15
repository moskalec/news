from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import PasswordResetFormCelery

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PasswordResetFormCelery),
         name='password_reset'),
    path('chat/', include('chat.urls', namespace='chat')),
    path('', include('django.contrib.auth.urls')),
    path('', include('posts.urls', namespace='posts')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
