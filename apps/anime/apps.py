from django.apps import AppConfig


class AnimeConfig(AppConfig):
    verbose_name = 'Приложение Anime'
    name = 'apps.anime'

    def ready(self):
        import apps.anime.signals