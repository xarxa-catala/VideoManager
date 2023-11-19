from rest_framework import viewsets, views, response
from .serializers import *
from dashboard.models import Show, Video
from django.shortcuts import get_object_or_404
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
    `GET /api/v2/videos/`\n
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
                        "app": "bool",
                        "videos": []
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


class ShowViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Show.objects.all().order_by('id')
        serializer = ShowSerializer(queryset, many=True, context={'exclude_fields': ['playlists']})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Show.objects.all().order_by('id')
        show = get_object_or_404(queryset, pk=pk)
        serializer = ShowSerializer(show)
        return response.Response(serializer.data)


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    def list(self, request):
        queryset = Playlist.objects.all().order_by('id')
        serializer = PlaylistSerializer(queryset, many=True, context={'exclude_fields': ['videos']})
        return response.Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Playlist.objects.all().order_by('id')
        show = get_object_or_404(queryset, pk=pk)
        serializer = PlaylistSerializer(show)
        return response.Response(serializer.data)


class PlaylistShowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(show__id=self.kwargs['show_id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['exclude_fields'] = ['videos']
        return context


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Video.objects.all().order_by('id')
    serializer_class = VideoSerializer


class VideoPlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        videos = Playlist.objects.filter(id=self.kwargs['playlist_id']).first().videos.all()
        return videos


class AppVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppVersion.objects.all().order_by('id')
    serializer_class = AppVersionSerializer
