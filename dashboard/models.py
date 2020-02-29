from django.db import models


# Create your models here.
class Show(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    nom_curt = models.CharField(max_length=MAX_LENGTH, unique=True, null=True)

    def __str__(self):
        return self.nom


class Season(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def __str__(self):
        return self.show.nom + " - " + self.nom


class VideoType(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return self.nom


class Video(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    episodi = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                help_text="Episodi associat a la preqüela o seqüela.")
    tipus = models.ForeignKey(VideoType, on_delete=models.CASCADE, null=True)
    url = models.URLField(max_length=MAX_LENGTH, unique=True)
    fitxer = models.FileField(max_length=MAX_LENGTH, null=True)
    thumbnail = models.ImageField(max_length=MAX_LENGTH, blank=True)
    encodar = models.BooleanField(default=False)
    subtitols = models.BooleanField(default=False)
