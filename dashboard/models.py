from django.db import models
from .utils.move_file import move_file, move_picture
from sortedm2m.fields import SortedManyToManyField


class Show(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    nom_curt = models.CharField(max_length=MAX_LENGTH, unique=True, null=True)
    ruta = models.CharField(max_length=MAX_LENGTH, default="")
    picture = models.ImageField(max_length=MAX_LENGTH, upload_to=move_picture, blank=True, null=True)

    def __str__(self):
        return self.nom


class Season(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    ruta = models.CharField(max_length=MAX_LENGTH,
                            help_text="Ruta de la temporada (sense incloure la sèrie).",
                            default="")

    def __str__(self):
        return self.show.nom + " - " + self.nom


class VideoType(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    ruta = models.CharField(max_length=MAX_LENGTH,
                            help_text="Ruta d'aquest tipus dins de cada sèrie.",
                            default="",
                            blank=True)

    def __str__(self):
        return self.nom


class Video(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH, null=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True)
    episodi = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="Episodi associat a la preqüela o seqüela.")
    tipus = models.ForeignKey(VideoType, on_delete=models.CASCADE, null=True)
    video_url = models.URLField(max_length=MAX_LENGTH, null=True, blank=True)
    fitxer = models.FileField(max_length=MAX_LENGTH, upload_to=move_file, null=True)
    encodar = models.BooleanField(default=False)
    subtitols = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Playlist(models.Model):
    MAX_LENGTH = 200
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=MAX_LENGTH)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
    videos = SortedManyToManyField(Video)
    app = models.BooleanField(default=False, help_text="Marca aquesta casella si vols que "
                                                       "la llista de reproducció sigui visible a l'app.")
    player = models.TextField(null=True)
