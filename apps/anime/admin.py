from django.contrib import admin
from .models import Anime, Episode, Genre, Studio, Still, PublishStatus, EpisodeVideo, VoiceStudio
from django.contrib import messages
from .forms import AddStillsAdminForm
from django.core.files.base import ContentFile
import zipfile

# admin.site.register(Anime)
# admin.site.register(Episode)


@admin.register(Still)
class StillAdmin(admin.ModelAdmin):
    list_display = ('id', 'anime')
    list_display_links = ('anime', )
    form = AddStillsAdminForm

    def save_model(self, request, obj, form, change):
        zip_file = form.cleaned_data.get('zip_file')
        if zip_file:
            with zipfile.ZipFile(zip_file) as zf:
                for name in zf.namelist():
                    if name.endswith('/'):
                        continue
                    elif name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        data = zf.read(name)
                        Still.objects.create(
                            anime=obj.anime,
                            image=ContentFile(data, name=name)
                        )
        else:
            super().save_model(request, obj, form, change)


class AgeRatingFilter(admin.SimpleListFilter):
    title = 'Возрастной рейтинг'
    parameter_name = 'age-rating'

    def lookups(self, request, modeladmin):
        return [
            ('adult', 'Для взрослых'),
            ('young', 'Для юных')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'adult':
            return queryset.filter(age_rating='18+')
        elif self.value() == 'young':
            return queryset.exclude(age_rating='18+')

# Кастомное действие над выбранными полями
@admin.action(description='Опубликовать выбранные аниме')
def publish(modeladmin, request, queryset):
    updated = queryset.update(publish_status=PublishStatus.PUBLISHED)
    modeladmin.message_user(
        request,
        f"Опубликовано: {updated}",
        messages.SUCCESS
    )

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publish_status', 'slug')
    list_display_links = ('id', 'title')
    list_editable = ('publish_status',)
    list_per_page = 10
    list_filter = (AgeRatingFilter, 'publish_status', 'status', )
    search_fields = ('title', )
    filter_horizontal = ('genres',)
    actions = [publish]

    fieldsets = (
    ('Обязательное', {
        'fields': ('title', 'format', 'release_year', 'release_season', 'age_rating', 'publish_status')
    }),
    ('Необязательное', {
        'fields': ('title_alter', 'slug', 'desc', 'genres', 'status', 'studio', 'poster')
    })
    )

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'anime', 'number', 'title')
    list_display_links = ('id', 'anime')
    list_filter = ('anime', )
    ordering = ('anime', 'number')
    search_fields = ('anime__title', 'number')
    autocomplete_fields = ('anime',)

@admin.register(EpisodeVideo)
class EpisodeVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'episode')
    autocomplete_fields = ('episode',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', )

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', )

@admin.register(VoiceStudio)
class VoiceStuioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')