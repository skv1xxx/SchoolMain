from django.shortcuts import render, redirect, get_object_or_404
from .forms import VideoForm, RegistrationForm, LoginForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .forms import PasswordResetRequestForm, PasswordResetConfirmForm
from .models import BDuser, PasswordResetToken

def index(request):
    videos = BDvid.objects.select_related('category').order_by('-publish_time')
    context = {
        'videos': videos
    }
    return render(request, 'index.html', context)


def design(request):
    return render(request, 'design/design.html')


def about_us(request):
    return render(request, 'about_us.html')

def kat(request):
    categories = BDkat.objects.all()
    return render(request, 'kat.html', {'categories': categories})

def search(request):
    return render(request, 'search.html')

def repass(request):
    return render(request, "repass.html")

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def acc(request):
    user = request.user
    context = {
        'user': user,
        'user_data': {
            'nickname': user.nickname,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'photo': user.photo,
        }
    }
    return render(request, 'acc.html', context)

def search(request):
    query = request.GET.get('q', '')
    videos = []

    if query:
        videos = BDvid.objects.select_related('category').filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-publish_time')

    context = {
        'query': query,
        'videos': videos,
    }
    return render(request, 'search.html', context)

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                video = form.save(commit=False)
                video.publish_time = timezone.now()
                video.save()
                messages.success(request, 'Видео успешно загружено!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке: {str(e)}')
    else:
        form = VideoForm()
    return render(request, 'addvid.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('acc')
    else:
        form = RegistrationForm()
    return render(request, 'reg.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = BDuser.objects.get(email=email)
                if user.check_password(password):
                    auth_login(request, user)
                    return redirect('acc')
                else:
                    form.add_error(None, "Неверный email или пароль")
            except BDuser.DoesNotExist:
                form.add_error(None, "Неверный email или пароль")
    else:
        form = LoginForm()
    return render(request, 'ent.html', {'form': form})

def video_detail(request, video_id):
    try:
        video = BDvid.objects.select_related('category').get(id=video_id)
    except BDvid.DoesNotExist:
        raise Http404("Видео не найдено")

    context = {
        'video': video,
    }
    return render(request, 'video_detail.html', context)

def category_videos(request, category_id):
    try:
        category = BDkat.objects.get(id=category_id)
        videos = BDvid.objects.filter(category=category).select_related('category').order_by('-publish_time')
        return render(request, 'category_videos.html', {
            'category': category,
            'videos': videos
        })
    except BDkat.DoesNotExist:
        raise Http404("Категория не найдена")


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            request.session['reset_email'] = email

            user = BDuser.objects.get(email=email)

            PasswordResetToken.objects.filter(
                user=user,
                is_used=False,
                expires_at__gt=timezone.now()
            ).update(is_used=True)

            token = PasswordResetToken.objects.create(user=user)

            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[token.token])
            )

            try:
                send_mail(
                    subject='Восстановление пароля',
                    message=f'Ссылка: {reset_url}',
                    html_message=f'',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Письмо с инструкциями отправлено на ваш email')
                return redirect('password_reset_done')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке письма: {str(e)}')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'password_reset_request.html', {'form': form})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def password_reset_confirm(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        if not reset_token.is_valid():
            messages.error(request, 'Ссылка для восстановления устарела или уже была использована')
            return redirect('password_reset_request')
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Недействительная ссылка для восстановления')
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            user = reset_token.user
            user.password = make_password(form.cleaned_data['new_password'])
            user.save()

            reset_token.is_used = True
            reset_token.save()

            messages.success(request, 'Пароль успешно изменен! Теперь вы можете войти.')
            return redirect('ent')
    else:
        form = PasswordResetConfirmForm()

    return render(request, 'password_reset_confirm.html', {
        'form': form,
        'user': reset_token.user
    })


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')