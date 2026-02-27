from django import template
from apps.anime.models import AnimeFormat, AnimeStatus, AgeRating

register = template.Library()

@register.simple_tag
def get_stills(anime, limit=4):
    return anime.stills.all()[:limit]

@register.simple_tag
def get_formats():
    return AnimeFormat.choices

@register.simple_tag
def get_statuses():
    return AnimeStatus.choices

@register.simple_tag
def get_age_ratings():
    return AgeRating.choices