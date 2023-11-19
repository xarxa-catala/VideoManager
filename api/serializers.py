from rest_framework import serializers
from dashboard.models import Show, Video, Playlist
from api.models import AppVersion
from VideoManager.constants import *
import os


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField('get_url')
    thumbnail = serializers.SerializerMethodField('get_thumbnail')
    cover = serializers.SerializerMethodField('get_cover')
    playlists = serializers.SerializerMethodField('get_playlists')

    class Meta:
        model = Show
        fields = ('id', 'nom', 'description', 'thumbnail', 'cover', 'url', 'playlists')

    def get_url(self, obj):
        return os.path.join(URL, obj.ruta)

    def get_thumbnail(self, obj):
        try:
            filename = os.path.basename(obj.picture.url)
            return os.path.join(URL, 'VideoManagerMedia', filename)
        except ValueError:
            return None

    def get_cover(self, obj):
        try:
            filename = os.path.basename(obj.picture_cover.url)
            return os.path.join(URL, 'VideoManagerMedia', filename)
        except ValueError:
            return None
    def get_playlists(self, obj):
        return Playlist.objects.filter(show__id=self.kwargs['show_id'])


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    class Meta:
        model = Video
        fields = ('id', 'nom', 'show_id', 'url')

    def get_url(self, obj):
        return obj.video_url


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):
    cover = serializers.SerializerMethodField('get_cover')
    class Meta:
        model = Playlist
        fields = ('id', 'nom', 'description', 'cover', 'show_id', 'app')

    def get_cover(self, obj):
        try:
            filename = os.path.basename(obj.picture.url)
            return os.path.join(URL, 'VideoManagerMedia', filename)
        except ValueError:
            return None


class AppVersionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppVersion
        fields = ('id', 'versionCode', 'versionString')
