from django.urls import include, path
from api.apps import ApiConfig
from rest_framework import routers
from . import views


class OptionalSlashRouter(routers.SimpleRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'shows/?', views.ShowViewSet)
router.register(r'shows/(?P<show_id>.+)/playlists/?', views.PlaylistShowViewSet, basename="shows")
router.register(r'playlists', views.PlaylistViewSet)
router.register(r'playlists/(?P<playlist_id>.+)/videos/?', views.VideoPlaylistViewSet, basename="playlists")
router.register(r'videos/?', views.VideoViewSet)
router.register(r'app/versions/?', views.AppVersionViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path(ApiConfig.version + '/', include(router.urls)),
    path(ApiConfig.version + '/', views.APIRoot.as_view()),
]
