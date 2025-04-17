from django.db import models
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return self.nickname

class BDvid(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    publish_time = models.DateTimeField(verbose_name="Время публикации")
    video_file = models.FileField(upload_to='videos/', verbose_name="Видео файл")
    category = models.ForeignKey('BDkat', on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["title"]

class BDkat(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("BDkat", kwargs={"BDkat_id":self.pk})
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"
        ordering = ["name"]