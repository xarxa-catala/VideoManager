import ffmpeg
import os
from VideoManager.constants import *
from pymediainfo import MediaInfo


def encode(instance, filename, output):
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

            ffmpeg.run(command)
            os.remove(os.path.join(MEDIA_ROOT_SAVED, instance.fitxer.name))
            instance.video_url = os.path.splitext(instance.video_url)[0] + ".mp4"
            instance.fitxer.name = os.path.splitext(instance.fitxer.name)[0] + ".mp4"
            instance.save()
            break
