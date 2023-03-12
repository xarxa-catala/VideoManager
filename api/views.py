from rest_framework import viewsets, views, response
from .serializers import *
from dashboard.models import Show, Season, VideoType, Video
from api.models import AppVersion


class APIRoot(views.APIView):
    """
    API de Xarxa Català\n
    Pots fer les següents consultes:\n
    `GET /api/v1/shows/`\n
    `GET /api/v1/shows/:show_id/seasons/`\n
    `GET /api/v1/shows/:show_id/films/`\n
    `GET /api/v1/shows/:show_id/extras/`\n
    `GET /api/v1/shows/:show_id/playlists/`\n
    `GET /api/v1/shows/:show_id/seasons/:season_id/episodes/`\n
    `GET /api/v1/shows/:show_id/seasons/:season_id/minisodes/`\n
    `GET /api/v1/shows/:show_id/playlists/:playlist_id/videos/`\n
    `GET /api/v1/videos/:video_id/`\n
    `GET /api/v1/app/versions/`\n

    Fent una crida GET a aquesta pàgina pots obtenir exemples de les consultes anteriors.
    """

    def get(self, request):
        data = {
            "show": [
                    {
                        "id": "int",
                        "nom": "string",
                        "url": "string",
                        "thumbnail": "string"
                    },
                ],
            "season": [
                    {
                        "id": "int",
                        "nom": "string",
                        "show_id": "int",
                        "url": "string"
                    },
                ],
            "video": [
                    {
                        "id": "int",
                        "nom": "string",
                        "show_id": "int",
                        "season_id": "int",
                        "url": "string",
                        "prequels": [],
                        "sequels": []
                    },
                ],
            "playlist": [
                    {
                        "id": "int",
                        "nom": "string",
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


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SeasonSerializer

    def get_queryset(self):
        seasons = Season.objects.filter(show__id=self.kwargs['show_id'])
        return seasons

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.filter(id=self.kwargs['video_id'])

class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        film_id = VideoType.objects.filter(ruta="Pelis")[0].id
        films = Video.objects.filter(show__id=self.kwargs['show_id']).filter(tipus__id=film_id)
        return films


class ExtraViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        extra_id = VideoType.objects.filter(ruta="Extres")[0].id
        extres = Video.objects.filter(show__id=self.kwargs['show_id']).filter(tipus__id=extra_id)
        return extres


class EpisodeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        episode_id = VideoType.objects.filter(ruta="")[0].id
        episodes = Video.objects.filter(show__id=self.kwargs['show_id'])\
            .filter(season__id=self.kwargs['season_id']).filter(tipus__id=episode_id)
        return episodes


class MinisodeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        minisode_id = VideoType.objects.filter(ruta="minisodes")[0].id
        minisodes = Video.objects.filter(show__id=self.kwargs['show_id'])\
            .filter(season__id=self.kwargs['season_id']).filter(tipus__id=minisode_id)
        return minisodes


class PlaylistViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        playlists = Playlist.objects.filter(show__id=self.kwargs['show_id'])
        return playlists


class PlaylistVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        videos = Playlist.objects.filter(id=self.kwargs['playlist_id']).first().videos.all()
        return videos


class AppVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppVersion.objects.all().order_by('id')
    serializer_class = AppVersionSerializer
