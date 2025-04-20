from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class BDuserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class BDuser(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    photo = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name', 'surname']

    objects = BDuserManager()

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return f"{self.name} {self.surname}"

    def get_short_name(self):
        return self.nickname

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["name"]

class BDvid(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    publish_time = models.DateTimeField(verbose_name="Время публикации")
    video_file = models.FileField(upload_to='videos/', verbose_name="Видео файл")
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        verbose_name="Превью видео",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    category = models.ForeignKey(
        'BDkat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория"
    )
    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ["title"]

    def get_thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return None

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail', args=[str(self.id)])

class BDkat(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
        verbose_name="Изображение категории",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("BDkat", kwargs={"BDkat_id": self.pk})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"
        ordering = ["name"]