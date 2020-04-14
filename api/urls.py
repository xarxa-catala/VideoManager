from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'shows', views.ShowViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/seasons', views.SeasonViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/films', views.FilmViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/extras', views.ExtraViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/seasons/(?P<season_id>.+)/episodes', views.EpisodeViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/seasons/(?P<season_id>.+)/minisodes', views.MinisodeViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/seasons/(?P<season_id>.+)/episodes/(?P<episode_id>.+)/prequels',
                views.PrequelViewSet, basename='api/v1')
router.register(r'shows/(?P<show_id>.+)/seasons/(?P<season_id>.+)/episodes/(?P<episode_id>.+)/sequels',
                views.SequelViewSet, basename='api/v1')

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('v1/', views.APIRoot.as_view()),
    path('v1/', include(router.urls)),
]
