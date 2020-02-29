from django.contrib import admin
from dashboard.models import Video, Show, Season, VideoType


# Register your models here.
class ShowAdmin(admin.ModelAdmin):
    list_display = ('nom_curt', 'nom')
    exclude = ()


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'show')
    exclude = ()


class VideoTypeAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    exclude = ()


class VideoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'url', 'thumbnail')
    readonly_fields = ('url',)
    exclude = ()


admin.site.register(Show, ShowAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(VideoType, VideoTypeAdmin)
admin.site.register(Video, VideoAdmin)
