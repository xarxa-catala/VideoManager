from django.contrib import admin
from dashboard.models import Video, Show, Playlist


# Register your models here.
class ShowAdmin(admin.ModelAdmin):
    list_display = ('nom_curt', 'nom', 'description', 'picture', 'picture_cover')


class VideoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'video_url')
    search_fields = ('nom',)


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'picture', 'show', 'app')


admin.site.register(Show, ShowAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Playlist, PlaylistAdmin)
