from django.contrib import admin

from .models import Category, Resp, Announcement

admin.site.register(Category)
admin.site.register(Resp)
admin.site.register(Announcement)
