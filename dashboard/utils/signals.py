from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch.dispatcher import receiver
from dashboard.models import Video
from .move_file import move_file
from VideoManager.constants import *
from django_q.tasks import async_task
import os


@receiver(pre_save, sender=Video)
def model_pre_save(sender, instance, **kwargs):
    try:
        instance._pre_save_instance = Video.objects.get(pk=instance.pk)
    except Video.DoesNotExist:
        instance._pre_save_instance = instance


@receiver(pre_save, sender=Video)
def delete_video_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).fitxer
    except sender.DoesNotExist:
        return False

    new_file = instance.fitxer
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_save, sender=Video)
def generate_url(sender, instance, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    prev_instance = instance._pre_save_instance
    if prev_instance.video_url == instance.video_url or prev_instance.fitxer != instance.fitxer:
        filename = os.path.basename(instance.fitxer.name)
        instance.video_url = os.path.join(URL, move_file(instance, filename))

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty


@receiver(post_save, sender=Video)
def encode(sender, instance, **kwargs):
    if hasattr(instance, '_dirty'):
        return

    filename = os.path.join(MEDIA_ROOT_SAVED, instance.fitxer.name)
    output = os.path.splitext(filename)[0] + ".mp4"

    if (instance.subtitols or instance.encodar) and not os.path.exists(output):
        async_task('dashboard.utils.tasks.encode', instance, filename, output,
                   task_name=instance.fitxer.name, q_options={'scheduler': False})

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty


# Delete the file when it is deleted from the admin panel.
@receiver(pre_delete, sender=Video)
def uploader_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.fitxer.delete(False)
