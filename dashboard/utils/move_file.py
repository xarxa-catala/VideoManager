import os


def move_file(instance, filename):
    return os.path.join(instance.show.ruta, filename)


def move_picture(instance, filename):
    return os.path.join('VideoManagerMedia', filename)
