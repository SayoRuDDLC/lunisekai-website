from django.db import models
from django.db.models import Count, Min, Max
from slugify import slugify
from django.shortcuts import reverse
import uuid
import random


'''
get_<choice>_display - чтобы выводить второе название в шаблоне (Черновик, Выходит и т.д.)
AnimeFormat(format_name).label - чтобы получить второе название в py-файле
'''


class AutoSlugMixin(models.Model):
    title_field = 'title'
    slug_field = 'slug'
    add_uuid = True

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        slug_value = getattr(self, self.slug_field, None)
        if not slug_value:
            title_value = getattr(self, self.title_field, '')
            if self.add_uuid:
                slug_value = f'{slugify(title_value)}-{uuid.uuid4().hex[:4]}'
            else:
                slug_value = f'{slugify(title_value)}'
            setattr(self, self.slug_field, slug_value)
        super().save(*args, **kwargs)


def still_upload_path(instance, filename):
    return f'anime/images/stills/{instance.anime.id}/{filename}'


def episode_upload_path(instance, filename):
    return f'anime/episodes/{instance.episode.anime.id}/{filename}'


class PublishStatus(models.TextChoices):
    DRAFT = 'draft', 'Черновик'
    PUBLISHED = 'published', 'Опубликовано'
    HIDDEN = 'hidden', 'Скрыто'


class AnimeStatus(models.TextChoices):
    UNKNOWN = 'unknown', 'Неизвестно'
    ANNOUNCED = 'announced', 'Анонсировано'
    ONGOING = 'ongoing', 'Выходит'
    COMPLETED = 'completed', 'Завершено'
    HIATUS = 'hiatus', 'Пауза'


class AnimeFormat(models.TextChoices):
    TV = 'tv', 'TV'
    OVA = 'ova', 'OVA'
    ONA = 'ona', 'ONA'
    MOVIE = 'movie', 'Фильм'
    SERIES = 'series', 'Сериал'
    SPECIAL = 'special', 'Спец. выпуск'


class ReleaseSeason(models.TextChoices):
    SPRING = 'spring', 'Весна'
    SUMMER = 'summer', 'Лето'
    AUTUMN = 'autumn', 'Осень'
    WINTER = 'winter', 'Зима'


class AgeRating(models.TextChoices):
    G = 'g', 'G'  # Нет возрастных ограничений
    PG = 'pg', 'PG'  # Рекомендуется присутствие взрослых
    PG13 = 'pg13', 'PG-13'  # Детям до 13 лет просмотр не желателен
    R17 = 'r17', 'R-17'  # Лицам до 17 лет обязательно присутствие взрослого
    R18 = 'r18', 'R-18'  # Лицам до 18 лет просмотр запрещен


# Кастомный QuerySet
class AnimeQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish_status=PublishStatus.PUBLISHED).order_by('created_at')

    def hidden(self):
        return self.filter(publish_status=PublishStatus.HIDDEN).order_by('created_at')

    def draft(self):
        return self.filter(publish_status=PublishStatus.DRAFT).order_by('created_at')

    def with_episodes_numbers(self):
        return self.prefetch_related(models.Prefetch(
            'episodes', queryset=Episode.objects.only('number', 'anime'), to_attr='episodes_numbers'
        ))

    def with_genres(self):
        """
        Оптимизация для получения жанров соответствующего аниме.
        Используется дополнительно Prefetch, чтобы отфильтровать жанры.
        Список (именно список, а не QuerySet, поэтому недоступны методы filter() и т.д. ) сохраняется в active_genres
        Обращение в django-шаблоне:
        {{ anime.active_genres }}

        Обычное использование prefetch_related():
        return self.prefetch_related('genres')

        prefetch_related должен использоваться при получении СПИСКА объектов из бд.
        При получении ток одного объекта - prefetch_related не нужен.
        """
        return self.prefetch_related(models.Prefetch(
            'genres', to_attr='active_genres'
        ))

    def with_episodes_count(self):
        return self.annotate(episodes_count=Count('episodes'))

    def random(self):
        count = self.count()

        if not count:
            return None

        random_offset = random.randint(0, count - 1)
        return self.order_by('id')[random_offset]


    def by_format(self, format):
        if format not in AnimeFormat.values:
            return self.none()
        return self.filter(format=format)

    def by_genre(self, genre_slug):
        return self.filter(genres__slug=genre_slug)

    def by_status(self, status):
        if status not in AnimeStatus.values:
            return self.none()
        return self.filter(status=status)

    def by_studio(self, studio):
        return self.filter(studio__slug=studio)

    def by_season(self, season, year):
        filters = {}

        if season is not None:
            if season not in ReleaseSeason.values:
                return self.none()
            filters['release_season'] = season

        if year is not None:
            filters['release_year'] = year

        return self.filter(**filters)

    def order_new(self):
        return self.order_by('-created_at')

    def order_updated(self):
        return self.order_by('-updated_at')


class Studio(AutoSlugMixin, models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')

    title_field = 'name'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('anime:anime_studio', kwargs={'studio_slug': self.slug})


class Still(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='stills', verbose_name='Аниме')
    image = models.ImageField(upload_to=still_upload_path, blank=True, verbose_name='Кадр')

    class Meta:
        verbose_name = 'Still'
        verbose_name_plural = 'Stills'

    def __str__(self):
        return f'Кадр из {self.anime.title}'


class Genre(AutoSlugMixin, models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')

    title_field = 'name'
    add_uuid = False

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('anime:anime_genre', kwargs={'genre_slug': self.slug})


class Anime(AutoSlugMixin, models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    title_alter = models.CharField(max_length=255, blank=True, verbose_name='Альтернативное название')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    desc = models.TextField(blank=True, verbose_name='Описание')
    format = models.CharField(
        max_length=20, choices=AnimeFormat.choices, default=AnimeFormat.TV, verbose_name='Формат'
    )
    genres = models.ManyToManyField(Genre, blank=True, related_name='anime', verbose_name='Жанры')
    release_year = models.PositiveSmallIntegerField(null=True, verbose_name='Год выхода')
    release_season = models.CharField(max_length=10, choices=ReleaseSeason.choices, default=ReleaseSeason.SPRING,
                                      verbose_name='Сезон выхода')
    status = models.CharField(max_length=15, choices=AnimeStatus.choices, default=AnimeStatus.UNKNOWN,
                              verbose_name='Статус')
    publish_status = models.CharField(
        max_length=10, choices=PublishStatus.choices, default=PublishStatus.DRAFT, verbose_name='Статус публикации'
    )
    age_rating = models.CharField(max_length=10, choices=AgeRating.choices, default=AgeRating.G,
                                  verbose_name='Возрастной рейтинг')
    studio = models.ForeignKey(
        Studio, on_delete=models.SET_NULL, blank=True, null=True, related_name='anime', verbose_name='Студия'
    )
    poster = models.ImageField(upload_to='anime/images/posters/', blank=True, null=True, verbose_name='Постер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    all_objects = models.Manager()  # Все объекты (стандартный менеджер)
    objects = AnimeQuerySet.as_manager()  # Только опубликованные (кастомный QuerySet представленный в виде менеджера)

    class Meta:
        verbose_name = 'Anime'  # Название в админке в ед. числе
        verbose_name_plural = 'Anime'  # Название в админке мн. числе
        indexes = [
            models.Index(fields=['title'], name='anime_title_idx'),
            models.Index(fields=['publish_status'], name='anime_publish_status_idx'),
        ]
        ordering = ['-created_at']  # Сначала новые

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('anime:anime_detail', kwargs={'anime_slug': self.slug})


class VoiceStudio(AutoSlugMixin, models.Model):
    name = models.CharField(max_length=255, verbose_name='Название студии')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')

    title_field = 'name'
    add_uuid = False

    def __str__(self):
        return self.name


class Episode(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes', verbose_name='Аниме')
    number = models.PositiveSmallIntegerField(verbose_name='Номер серии')
    title = models.CharField(max_length=255, blank=True, verbose_name='Название серии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        ordering = ['number']
        unique_together = ('anime', 'number')

    def __str__(self):
        return f'{self.anime.title} - серия {self.number}'


class EpisodeVideo(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name='videos', verbose_name='Эпизод')
    video = models.FileField(upload_to=episode_upload_path, verbose_name='Видео', null=True)
    voice = models.ForeignKey(VoiceStudio, on_delete=models.SET_NULL, null=True, related_name='videos',
                              verbose_name='Озвучка')

    def __str__(self):
        return f'{self.episode} - {self.voice}'
