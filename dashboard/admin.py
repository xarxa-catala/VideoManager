from django.contrib import admin
from dashboard.models import Video


# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'url', 'thumbnail')
    exclude = ()


admin.site.register(Video, VideoAdmin)
