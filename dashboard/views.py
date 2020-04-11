from django.http import JsonResponse
from dashboard.utils.encoding_queue import queue


def queue_view(request):
    queue_list = list(queue.queue)
    data = []
    for q in queue_list:
        data.append(str(q)[str(q).find("filename"):str(q).find(' ', str(q).find("filename"))-1])

    return JsonResponse(data, safe=False)
