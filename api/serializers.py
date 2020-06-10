from rest_framework import serializers
from dashboard.models import Show, Season, Video, VideoType
from VideoManager.constants import *
import os


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField('get_url')
    thumbnail = serializers.SerializerMethodField('get_thumbnail')

    class Meta:
        model = Show
        fields = ('id', 'nom', 'thumbnail', 'url')

    def get_url(self, obj):
        return os.path.join(URL, obj.ruta)

    def get_thumbnail(self, obj):
        try:
            filename = os.path.basename(obj.picture.url)
        except ValueError:
            filename = "default.jpg"
        return os.path.join(URL, 'VideoManagerMedia', filename)


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Season
        fields = ('id', 'nom', 'show_id', 'url')

    def get_url(self, obj):
        return os.path.join(URL, obj.ruta)


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField('get_url')
    prequels = serializers.SerializerMethodField('get_prequels')
    sequels = serializers.SerializerMethodField('get_sequels')

    class Meta:
        model = Video
        fields = ('id', 'nom', 'show_id', 'season_id', 'url', 'prequels', 'sequels')

    def get_url(self, obj):
        return obj.video_url

    def get_prequels(self, obj):
        prequel_id = VideoType.objects.filter(ruta="prequels")[0].id
        prequels = [{"id": v.id, "nom": v.nom, "url": v.video_url}
                    for v in obj.video_set.all() if v.tipus.id == prequel_id]
        return prequels

    def get_sequels(self, obj):
        sequel_id = VideoType.objects.filter(ruta="sequels")[0].id
        sequels = [{"id": v.id, "nom": v.nom, "url": v.video_url}
                    for v in obj.video_set.all() if v.tipus.id == sequel_id]
        return sequels
