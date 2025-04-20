from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('design/', views.design, name='design'),
    path('about_us/', views.about_us, name='about_us'),
    path('acc/', login_required(views.acc), name='acc'),
    path('kat/', views.kat, name='kat'),
    path('search/', views.search, name='search'),
    path('repass/', views.repass, name='repass'),
    path('upload/', login_required(views.upload_video), name='upload'),
    path('reg/', views.register, name='reg'),
    path('ent/', views.login_view, name='ent'),
    path('logout/', views.logout_view, name='logout'),
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('category/<int:category_id>/', views.category_videos, name='category_videos'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)