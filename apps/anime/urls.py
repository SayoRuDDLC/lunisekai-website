from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.SeasonConverter, 'season')

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('anime/', views.AnimeListView.as_view(), name='anime_list'),
    path('anime/random-anime/', views.AnimeRandomView.as_view(), name='anime_random'),
    path('anime/format/<slug:format_slug>/', views.AnimeFormatView.as_view(), name='anime_format'),
    path('anime/genre/<slug:genre_slug>/', views.AnimeGenreView.as_view(), name='anime_genre'),
    path('anime/status/<slug:status_slug>/', views.AnimeStatusView.as_view(), name='anime_status'),
    path('anime/studio/<slug:studio_slug>/', views.AnimeStudioView.as_view(), name='anime_studio'),
    path('anime/year/<int:year>/', views.AnimeSeasonView.as_view(), name='anime_year'),
    path('anime/season/<season:season>/', views.AnimeSeasonView.as_view(), name='anime_season'),
    path('anime/season/<season:season>/<int:year>/', views.AnimeSeasonView.as_view(), name='anime_season_and_year'),
    path('anime/add-anime/', views.AnimeEditorView.as_view(), name='add_anime'),
    path('anime/<slug:anime_slug>/', views.AnimeDetailView.as_view(), name='anime_detail'),
    path('manga/', views.MangaListView.as_view(), name='manga_list'),
    path('light-novels/', views.NovelListView.as_view(), name='novel_list')
]