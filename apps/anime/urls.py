from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('anime/', views.anime_list, name='anime_list'),
    path('anime/random-anime/', views.anime_random, name='anime_random'),
    path('anime/format/<slug:format_slug>/', views.anime_format, name='anime_format'),
    path('anime/genre/<slug:genre_slug>/', views.anime_genre, name='anime_genre'),
    path('anime/status/<slug:status_slug>/', views.anime_status, name='anime_status'),
    path('anime/studio/<slug:studio_slug>/', views.anime_studio, name='anime_studio'),
    path('anime/year/<int:year>/', views.anime_season, name='anime_year'),
    path('anime/season/<slug:season_slug>/', views.anime_season, name='anime_season'),
    path('anime/season/<slug:season_slug>/<int:year>/', views.anime_season, name='anime_season_and_year'),
    path('anime/add-anime/', views.add_anime, name='add_anime'),
    path('anime/<slug:anime_slug>/', views.anime_detail, name='anime_detail'),
    path('manga/', views.manga_list, name='manga_list'),
    path('light-novels/', views.novel_list, name='novel_list')
]