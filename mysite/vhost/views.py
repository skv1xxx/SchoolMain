from django.shortcuts import render, redirect
from .forms import VideoForm, RegistrationForm, LoginForm
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.db.models import Q


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