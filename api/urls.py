from django.urls import include, path
from api.apps import ApiConfig
from rest_framework import routers
from . import views

api_basename = ApiConfig.name + '/' + ApiConfig.version
router = routers.SimpleRouter()
router.register(r'shows/(?P<show_id>.+)/playlists', views.PlaylistViewSet, basename=api_basename)
router.register(r'shows/(?P<show_id>.+)', views.SingleShowViewSet, basename=api_basename)
router.register(r'shows', views.ShowViewSet, basename=api_basename)
router.register(r'playlists/(?P<playlist_id>.+)/videos', views.VideoViewSet, basename=api_basename)
router.register(r'playlists/(?P<playlist_id>.+)', views.SinglePlaylistViewSet, basename=api_basename)
router.register(r'playlists', views.PlaylistViewSet, basename=api_basename)
router.register(r'videos/(?P<video_id>.+)', views.VideoViewSet, basename=api_basename)
router.register(r'app/versions', views.AppVersionViewSet, basename=api_basename)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path(ApiConfig.version + '/', views.APIRoot.as_view()),
    path(ApiConfig.version + '/', include(router.urls)),
]
