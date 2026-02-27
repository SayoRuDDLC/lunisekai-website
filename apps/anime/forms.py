from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Anime, Genre, PublishStatus, Still


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'абвгд'
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Разрешаются ток русские символы'

    def __call__(self, value, *args, **kwargs):
        if not (set(value).issubset(self.ALLOWED_CHARS)): # Проверка является ли value подмножеством ALLOWED_CHARS
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
    class Meta:
        model = Anime
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == 'anime':
            raise forms.ValidationError('Низя такое название!')
        return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if title == 'anime':
            raise forms.ValidationError('Ыыыыыы!')

    '''
    form.title - поле формы
    form.title.label - лейбл поля формы
    form.title.errors - ошибки поля формы
    form.non_field_errors - ошибки не касающиеся полей формы
    
    <form action="" method="POST" novalidate> - чтобы отключить HTML5 валидацию в форме
    '''

class TestForm(forms.Form):
    title = forms.CharField(validators=[
        MinLengthValidator(3, message='Минимальное колво символов - 3'),
        MaxLengthValidator(10, message='Максимальное колво символов - 10'),
        RussianValidator(),
    ], error_messages={
        'required': 'Обязательно для заполнения'
    })
    subtittle = forms.CharField(
        max_length=10,
        min_length=5, label='Субтитл', required=True, initial='Ну типа субтитл',
        error_messages={
            'min_length': 'Минимум 5 символов ыыыы'
        }
    )
    category = forms.ModelChoiceField(queryset=Genre.objects.all(), empty_label='Не выбрана категория', label='Категория')
