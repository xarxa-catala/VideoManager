from django.contrib import admin
from dashboard.models import Video, Show, Season, VideoType


# Register your models here.
class ShowAdmin(admin.ModelAdmin):
    list_display = ('nom_curt', 'nom')


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'show')


class VideoTypeAdmin(admin.ModelAdmin):
    list_display = ('nom',)


class VideoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'video_url', 'thumbnail')
    readonly_fields = ('video_url',)


admin.site.register(Show, ShowAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(VideoType, VideoTypeAdmin)
admin.site.register(Video, VideoAdmin)
