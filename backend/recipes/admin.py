from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)
