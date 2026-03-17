from apps.anime.models import ReleaseSeason


class SeasonConverter:
    regex = 'spring|summer|autumn|winter'

    # Например, 'anime/season/winter' => ReleaseSeason('winter') => ReleaseSeason.WINTER
    def to_python(self, value):
        return ReleaseSeason(value)

    # Например, 'season': 'winter' => 'value' = 'season' => return 'winter'
    def to_url(self, value):
        if isinstance(value, ReleaseSeason): # Если передали объект ReleaseSeason
            return value.value
        # Если передали строку, например anime.release_season => 'winter'
        return value