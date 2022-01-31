from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "first_name", "last_name")
    search_fields = ("email", "username")
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.site_title = "Foodgram"
admin.site.site_header = "Foodgram"