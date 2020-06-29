from django.db import models


class AppVersion(models.Model):
    MAX_LENGTH = 20
    id = models.AutoField(primary_key=True)
    versionCode = models.IntegerField()
    versionString = models.CharField(max_length=MAX_LENGTH)
