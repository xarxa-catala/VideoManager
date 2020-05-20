from rest_framework import viewsets, views, response
from .serializers import *
from dashboard.models import Show, Season, VideoType, Video


class APIRoot(views.APIView):
    """
    API de Xarxa Català\n
    Pots fer les següents consultes:\n
    `GET /api/v1/shows/`\n
    `GET /api/v1/shows/:show_id/seasons`\n
    `GET /api/v1/shows/:show_id/films/`\n
    `GET /api/v1/shows/:show_id/extras/`\n
    `GET /api/v1/shows/:show_id/seasons/:season_id/episodes/`\n
    `GET /api/v1/shows/:show_id/seasons/:season_id/minisodes/`\n

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
