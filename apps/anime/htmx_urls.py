from django.urls import path
from . import htmx_views

app_name = 'htmx'

urlpatterns = [
    path('get-desc/<slug:anime_slug>', htmx_views.get_desc, name='get_desc'),
    path('get-episode/<slug:anime_slug>/<int:episode_number>', htmx_views.get_episode, name='get_episode'),
    path('edit-anime/<slug:anime_slug>', htmx_views.edit_anime, name='edit_anime'),
]