from .models import *
from .forms import *
from django.shortcuts import render, redirect
from .forms import VideoForm

def index(request):
    return render(request, 'index.html')

def design(request):
    return render(request, 'design/design.html')

def about_us(request):
    return render(request, 'about_us.html')

def acc(request):
    return render(request, 'acc.html')

def kat(request):
    return render(request, 'kat.html')

def search(request):
    return render(request, 'search.html')

def reg(request):
    return render(request, "reg.html")

def ent(request):
    return render(request,'ent.html')

def repass(request):
    return render(request,"repass.html")


def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Замените на ваш URL успешной загрузки
    else:
        form = VideoForm(initial={'publish_time': timezone.now()})

    return render(request, 'addvid.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'reg.html', {'form': form})