import os


def move_file(instance, filename):
    if instance.season is None:
        final_path = os.path.join(instance.show.ruta, instance.tipus.ruta, filename)
    else:
        final_path = os.path.join(instance.show.ruta, instance.season.ruta, instance.tipus.ruta, filename)

    return final_path
