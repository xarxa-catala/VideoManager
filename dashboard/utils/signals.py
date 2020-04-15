from django.db.models.signals import pre_save, post_save, pre_delete, m2m_changed
from django.dispatch.dispatcher import receiver
from dashboard.models import Video, Playlist
from .move_file import move_file
from VideoManager.constants import *
from VideoManager.settings import BASE_DIR
from pymediainfo import MediaInfo
from .encoding_queue import queue, do_encode
from threading import Thread
import ffmpeg
import os


@receiver(pre_save, sender=Video)
def generate_url(sender, instance, **kwargs):
    filename = os.path.basename(instance.fitxer.name)
    instance.video_url = os.path.join(URL, move_file(instance, filename))


@receiver(post_save, sender=Video)
def encode(sender, instance, **kwargs):
    filename = os.path.join(MEDIA_ROOT_SAVED, instance.fitxer.name)
    output = os.path.splitext(filename)[0] + ".mp4"

    if (instance.subtitols or instance.encodar) and not os.path.exists(output):
        input_file = ffmpeg.input(filename)
        audio = input_file.audio
        video = input_file.video

        for track in MediaInfo.parse(filename).tracks:
            if track.track_type == 'Video':
                if instance.subtitols:
                    command = ffmpeg.output(audio, video, output,
                                        acodec="libmp3lame",
                                        vcodec="libx264",
                                        vf='subtitles=' + filename)
                elif track.writing_library is None:
                    command = ffmpeg.output(audio, video, output, acodec="libmp3lame", vcodec="libx264")
                elif track.writing_library.startswith("x264"):
                    command = ffmpeg.output(audio, video, output, acodec="libmp3lame", vcodec="copy")
                else:
                    command = ffmpeg.output(audio, video, output, acodec="libmp3lame", vcodec="libx264")
                queue.put(command)
                worker = Thread(target=do_encode, args=[queue, instance], daemon=True)
                worker.start()
                break


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
        instance.player = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.0/jquery.min.js"></script>' \
                          '<script>$(function(){$("#includedContent").' \
                          'load("https://gestio.multimedia.xarxacatala.cat/player/html/' + filename + '");' \
                          '});</script><div id="includedContent"></div>'
        instance.save()
