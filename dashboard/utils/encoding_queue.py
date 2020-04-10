from VideoManager.constants import *
from queue import Queue
import ffmpeg
import os


def do_encode(q, instance):
    if q.qsize() > 1:
        q.join()
    else:
        ffmpeg.run(q.get())
        os.remove(os.path.join(MEDIA_ROOT_SAVED, instance.fitxer.name))
        instance.video_url = os.path.splitext(instance.video_url)[0] + ".mp4"
        instance.fitxer.name = os.path.splitext(instance.fitxer.name)[0] + ".mp4"
        instance.save()
        q.task_done()


queue = Queue(maxsize=0)
