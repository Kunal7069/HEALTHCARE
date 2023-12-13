"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from mysite.consumer import VideoConsumer
websocket_urlpatterns = [
    re_path(r'ws/video_stream/', VideoConsumer.as_asgi()),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('camera/', views.camera),
    path('', views.home_2),
    path('detail/', views.detail),
    path('find/', views.find),
    path('video_feed', views.video_feed, name='video_feed'),
    # path('video_feed_2/', views.video_feed_2, name='video_feed_2')
    
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 