from django.contrib import admin

from .models import Tag, Recipe, Ingredient, ShoppingCart, Favorite


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author")
    ordering = ("pk",)
    list_filter = ("name", "author__username", "tags__name")
    empty_value_display = "-пусто-"
    readonly_fields = ("recipe_count",)

    def recipe_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    recipe_count.short_description = 'Количество добавлений в избранное'


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
