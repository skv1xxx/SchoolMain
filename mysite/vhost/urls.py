from django.urls import path
from . import views
from .views import design
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('design', views.design),
    path('about_us', views.about_us),
    path("home", views.index),
    path('acc', views.acc),
    path('kat', views.kat),
    path('search', views.search),
    path("reg", views.reg, name="reg"),
    path("ent",views.ent, name="ent"),
    path("repass",views.repass, name="repass"),
    path('upload', views.upload_video, name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
