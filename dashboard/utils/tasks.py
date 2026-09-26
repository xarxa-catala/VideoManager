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
                                        acodec="libopus",
                                        vcodec="libvpx-vp9",
                                        crf=30,
                                        **{
                                            'b:v': '0',
                                            'b:a': '128k'
                                        },
                                        vf='subtitles=' + filename)
            else:
                command = ffmpeg.output(audio, video, output,
                                        acodec="libopus",
                                        vcodec="libvpx-vp9", 
                                        **{
                                            'b:v': '0',
                                            'b:a': '128k'
                                        },
                                        crf=30)

            ffmpeg.run(command)
            os.remove(os.path.join(MEDIA_ROOT_SAVED, instance.fitxer.name))
            instance.video_url = os.path.splitext(instance.video_url)[0] + ".webm"
            instance.fitxer.name = os.path.splitext(instance.fitxer.name)[0] + ".webm"
            instance.save()
            break
