from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver
from dashboard.models import Video
from .move_file import move_file
from VideoManager.constants import *
import os


@receiver(pre_save, sender=Video)
def generate_url(sender, instance, **kwargs):
    filename = os.path.basename(instance.fitxer.name)
    instance.video_url = os.path.join(URL, move_file(instance, filename))
