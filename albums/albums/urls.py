"""
URL configuration for albums project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework_nested import routers
from api.views import AlbumViewSet, SongViewSet

# 1. Create a standard router for the Parent (Album)
router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet, basename='albums')
# This gives you "Selective" access: /api/songs/5/
router.register(r'songs', SongViewSet, basename='all-songs')

# 2. Create the Nested Router for the Child (Songs)
# 'albums' is the lookup prefix used in the parent router
albums_router = routers.NestedDefaultRouter(router, r'albums', lookup='album')
albums_router.register(r'songs', SongViewSet, basename='album-songs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(albums_router.urls)),
]
