from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch.dispatcher import receiver
from dashboard.models import Video, Playlist
from .move_file import move_file
from VideoManager.constants import *
from VideoManager.settings import BASE_DIR
from django_q.tasks import async_task
import os


@receiver(post_save, sender=Video)
def generate_url(sender, instance, **kwargs):
    if hasattr(instance, '_dirty'):
        return

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
        async_task('dashboard.utils.tasks.encode', instance, filename, output, task_name=instance.fitxer.name)

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


@receiver(m2m_changed, sender=Playlist.videos.through)
def create_player(sender, instance, **kwargs):
    if kwargs.get('action') == 'post_add':  # Do not trigger twice.
        content = open(os.path.join(BASE_DIR, "dashboard/player/html/index.html"), "r").readlines()
        ul_tags = [i for i, l in enumerate(content) if "<ul id" in l][0]

        for video in instance.videos.all():
            html_li = '<li>\n<a href="#" class="video_player_chapter" data-vsource="' + video.video_url + '">'
            html_li += video.nom + '</a>\n</li>\n'
            content.insert(ul_tags + 1, html_li)
            ul_tags += 1

        filename = "player-" + str(instance.id) + ".html"
        player_html = open(os.path.join('dashboard/player/html/', filename), 'w')
        player_html.write(''.join(content))
        instance.player = '<script src="https://gestio.multimedia.xarxacatala.cat/player/js/jquery.min.js"></script>' \
                          '<script>$(function(){$("#includedContent").' \
                          'load("https://gestio.multimedia.xarxacatala.cat/player/html/' + filename + '");' \
                          '});</script><div id="includedContent"></div>'
        instance.save()
