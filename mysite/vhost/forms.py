from django import forms
from .models import *
from django import forms
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class VideoForm(forms.ModelForm):
    class Meta:
        model = BDvid
        fields = ['title', 'description', 'publish_time', 'video_file', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название видео'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание видео',
                'rows': 4
            }),
            'publish_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'kat': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Не менее 8 символов'}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}),
    )

    class Meta:
        model = CustomUser
        fields = ('nickname', 'first_name', 'last_name', 'email', 'avatar', 'password1', 'password2')
        widgets = {
            'nickname': forms.TextInput(attrs={'placeholder': 'Ваш уникальный ник'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@mail.com'}),
        }