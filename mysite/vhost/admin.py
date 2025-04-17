from django.contrib import admin
from .models import *


class BDkatAD(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(CustomUser)
admin.site.register(BDvid)
admin.site.register(BDkat, BDkatAD)
