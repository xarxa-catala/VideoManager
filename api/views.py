from rest_framework import viewsets, views, response
from .serializers import *
from dashboard.models import Show, Season, VideoType, Video


class APIRoot(views.APIView):
    """
    API de Xarxa Català
    """
    # http_method_names = ['get']

    def get(self, request):
        data = {
            "shows": "https://multimedia.xarxacatala.cat/shows/",
            "groups": "http://localhost:8000/groups/",
            "users": "http://localhost:8000/schedules/",
        }

        if not request.user.is_superuser:
            data.pop("users")
            data.pop("groups")

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
