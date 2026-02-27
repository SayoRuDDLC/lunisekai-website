from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, Http404
from .models import Anime, Episode
from functools import wraps

def htmx_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('HX-Request'):
            raise Http404()
        return view_func(request, *args, **kwargs)

    return wrapper

@htmx_only
def get_desc(request, anime_slug):
    full = request.GET.get('full') == 'true'
    anime = get_object_or_404(
        Anime.objects.published().only('desc'),
        slug=anime_slug,
    )
    template = 'anime/includes/anime_full_desc.html' if full else 'anime/includes/anime_short_desc.html'
    return render(request, template, {'anime': anime})


@htmx_only
def get_episode(request, anime_slug, episode_number):
    voice_slug = request.GET.get('voice')
    episode = get_object_or_404(Episode, anime__slug=anime_slug, number=episode_number)

    videos = episode.videos.all()
    if voice_slug:
        video = get_object_or_404(videos, voice__slug=voice_slug)
    else:
        video = videos.first()

    return render(
        request, 'anime/includes/anime_player.html',
        context={
            'episode': episode,
            'video': video,
            'videos': videos,
            'active_voice_slug': voice_slug,
        }
    )

