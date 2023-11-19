from rest_framework import viewsets, views, response
from .serializers import *
from dashboard.models import Show, Video
from api.models import AppVersion


class APIRoot(views.APIView):
    """
    API de Xarxa Català\n
    Pots fer les següents consultes:\n
    `GET /api/v2/shows/`\n
    `GET /api/v2/shows/:show_id/`\n
    `GET /api/v2/shows/:show_id/playlists/`\n
    `GET /api/v2/playlists/`\n
    `GET /api/v2/playlists/:playlist_id/`\n
    `GET /api/v2/playlists/:playlist_id/videos/`\n
    `GET /api/v2/videos/:video_id/`\n
    `GET /api/v2/app/versions/`\n

    Fent una crida GET a aquesta pàgina pots obtenir exemples de les consultes anteriors.
    """

    def get(self, request):
        data = {
            "show": [
                    {
                        "id": "int",
                        "nom": "string",
                        "description": "string",
                        "url": "string",
                        "thumbnail": "string",
                        "cover": "string",
                        "playlists": []
                    },
                ],
            "video": [
                    {
                        "id": "int",
                        "nom": "string",
                        "show_id": "int",
                        "url": "string"
                    },
                ],
            "playlist": [
                    {
                        "id": "int",
                        "nom": "string",
                        "description": "string",
                        "cover": "string",
                        "show_id": "int",
                        "app": "bool"
                    }
                ],
            "version": [
                    {
                        "id": "int",
                        "versionCode": "int",
                        "versionString": "string"
                    }
                ],
        }

        return response.Response(data)


class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Show.objects.all().order_by('id')
    serializer_class = ShowSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['exclude_fields'] = ['playlists']
        return context


class SingleShowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ShowSerializer

    def get_queryset(self):
        return Show.objects.filter(id=self.kwargs['show_id'])


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.filter(id=self.kwargs['video_id'])


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        try:
            playlists = Playlist.objects.filter(id=self.kwargs['playlist_id'])
        except KeyError:
            playlists = Playlist.objects.all().order_by('id')
        return playlists


class PlaylistVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        videos = Playlist.objects.filter(id=self.kwargs['playlist_id']).first().videos.all()
        return videos


class AppVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppVersion.objects.all().order_by('id')
    serializer_class = AppVersionSerializer
