from django.urls import path
from . import views

urlpatterns = [
    path('cua/', views.queue_view),
]
