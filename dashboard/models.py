from django.db import models


# Create your models here.
class Video(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    url = models.URLField(max_length=MAX_LENGTH, unique=True)
    thumbnail = models.ImageField(max_length=MAX_LENGTH, blank=True)
