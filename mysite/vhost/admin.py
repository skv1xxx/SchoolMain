from django.contrib import admin
from .models import *

class BDkatAD(admin.ModelAdmin):
    list_display = ('id', 'name')
    actions = ['delete_category']

    def delete_category(self, request, queryset):
        for category in queryset:
            BDvid.objects.filter(category=category).update(category=None)
            category.delete()

    delete_category.short_description = "Delete selected categories (safely)"

admin.site.register(BDuser)
admin.site.register(BDvid)
admin.site.register(BDkat, BDkatAD)