from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible
import textwrap

from .models import Anime, Genre, PublishStatus, Still, ReleaseSeason, Studio


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'абвгд'
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Разрешаются ток русские символы'

    def __call__(self, value, *args, **kwargs):
        if not (set(value).issubset(self.ALLOWED_CHARS)):  # Проверка является ли value подмножеством ALLOWED_CHARS
            raise ValidationError(self.message, code=self.code)


class AddStillsAdminForm(forms.ModelForm):
    zip_file = forms.FileField(required=False, help_text='Загрузите ZIP с кадрами.', label='ZIP файл')

    class Meta:
        model = Still
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anime'].empty_label = '— Выберите аниме —'

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        zip_file = cleaned_data.get('zip_file')

        if not image and not zip_file:
            raise forms.ValidationError('Вы должны загрузить либо изображение, либо ZIP файл с изображениями.')

        return cleaned_data

class AddAnimeForm(forms.ModelForm):
    studio = forms.ModelChoiceField(
        queryset=Studio.objects.all(),
        widget=forms.Select(attrs={'id': 'form__studio'}),
        empty_label='Неизвестно',
        label='Студия',
        required=False,
    )

    class Meta:
        model = Anime
        fields = [
            'title', 'title_alter', 'slug', 'desc', 'format', 'genres', 'release_year', 'release_season',
            'status', 'publish_status', 'age_rating', 'studio', 'poster'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'form__title',
                'placeholder': 'Наруто: Ураганные хроники'
            }),
            'title_alter': forms.TextInput(attrs={
                'id': 'form__title-alter',
                'placeholder': 'Naruto: Shippuuden'
            }),
            'slug': forms.TextInput(attrs={
                'id': 'form__slug',
                'placeholder': 'naruto-uragannye-khroniki'
            }),
            'desc': forms.Textarea(attrs={
                'id': 'form__desc',
                'placeholder': '«Ураганные хроники» продолжают историю о приключениях юного ниндзя Наруто Узумаки и '
                               'его друзей. С начала серии проходит три года, герои взрослеют, набираются жизненного '
                               'опыта и совершенствуют свои навыки. Наруто возвращается в Деревню Скрытой Листвы, и '
                               'команда, ранее состоящая из него, Саскэ и Сакуры , переформировывается. Место Саскэ в '
                               'ней занимает молодой ниндзя по имени Сай, и вместе они берут название '
                               '«Команда Какаши». Но безоблачная жизнь длится недолго...',
                'rows': 3,
                'cols': 20
            }),
            'format': forms.RadioSelect(attrs={
                'id': 'form__format',

            }),
            'genres': forms.CheckboxSelectMultiple(attrs={
                'id': 'form__genres'
            }),
            'release_year': forms.NumberInput(attrs={
                'id': 'form__release-year',
                'placeholder': '2007',
                'min': 0,
            }),
            'release_season': forms.RadioSelect(attrs={
                'id': 'form__release-season',
            }),
            'status': forms.RadioSelect(attrs={
                'id': 'form__status',
            }),
            'publish_status': forms.RadioSelect(attrs={
                'id': 'form__publish-status',
            }),
            'age_rating': forms.RadioSelect(attrs={
                'id': 'form__age-rating',
            }),
            'poster': forms.FileInput(attrs={
                'id': 'form__poster',
            })
        }

        required_error_message = 'Данное поле является обязательным для заполнения.'
        invalid_choice_error_message = 'Данное значение является недопустимым.'
        invalid_error_message = 'Некорректные данные'
        error_messages = {
            'title': {
                'required': required_error_message,
            },
            'release_year': {
                'required': required_error_message,
                'invalid': invalid_error_message
            },
            'release_season': {
                'required': required_error_message,
                'invalid_choice': invalid_choice_error_message,
            },
            'format': {
                'required': required_error_message,
                'invalid_choice': invalid_choice_error_message,
            },
            'age_rating': {
                'required': required_error_message,
                'invalid_choice': invalid_choice_error_message,
            },
            'publish_status': {
                'required': required_error_message,
                'invalid_choice': invalid_choice_error_message,
            }
        }

    # class TestAddAnimeForm(forms.ModelForm):
    #     class Meta:
    #         model = Anime
    #         fields = '__all__'
    #         widgets = {
    #             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
    #         }
    #
    #     def clean_title(self):
    #         title = self.cleaned_data.get('title')
    #         if title == 'anime':
    #             raise forms.ValidationError('Низя такое название!')
    #         return title
    #
    #     def clean(self):
    #         cleaned_data = super().clean()
    #         title = cleaned_data.get('title')
    #         if title == 'anime':
    #             raise forms.ValidationError('Ыыыыыы!')

    '''
    form.title - поле формы
    form.title.label - лейбл поля формы
    form.title.errors - ошибки поля формы
    form.non_field_errors - ошибки не касающиеся полей формы
    
    <form action="" method="POST" novalidate> - чтобы отключить HTML5 валидацию в форме
    '''
#
# class TestForm(forms.Form):
#     title = forms.CharField(validators=[
#         MinLengthValidator(3, message='Минимальное колво символов - 3'),
#         MaxLengthValidator(10, message='Максимальное колво символов - 10'),
#         RussianValidator(),
#     ], error_messages={
#         'required': 'Обязательно для заполнения'
#     })
#     subtittle = forms.CharField(
#         max_length=10,
#         min_length=5, label='Субтитл', required=True, initial='Ну типа субтитл',
#         error_messages={
#             'min_length': 'Минимум 5 символов ыыыы'
#         }
#     )
#     category = forms.ModelChoiceField(queryset=Genre.objects.all(), empty_label='Не выбрана категория', label='Категория')
