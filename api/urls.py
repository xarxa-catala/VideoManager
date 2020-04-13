from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'shows', views.ShowViewSet)
router.register(r'shows/(?P<show_id>.+)/seasons', views.SeasonViewSet, basename='api')
router.register(r'shows/(?P<show_id>.+)/films', views.FilmViewSet, basename='api')
router.register(r'shows/(?P<show_id>.+)/extras', views.ExtraViewSet, basename='api')
router.register(r'shows/(?P<show_id>.+)/seasons/(?P<season_id>.+)/episodes', views.EpisodeViewSet, basename='api')


# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', views.APIRoot.as_view()),
    path('', include(router.urls)),
]
