from django.contrib import admin
from api.models import AppVersion


class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('versionCode', 'versionString')


admin.site.register(AppVersion, AppVersionAdmin)
