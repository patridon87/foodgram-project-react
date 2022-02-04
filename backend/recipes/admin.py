from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author")
    ordering = ("pk",)
    search_fields = (
        "name",
        "author__username",
    )
    list_filter = ("tags__name",)
    empty_value_display = "-пусто-"
    readonly_fields = ("recipe_count",)

    def recipe_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    recipe_count.short_description = "Количество добавлений в избранное"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    ordering = ("pk",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "recipe", "amount")
    ordering = ("pk",)
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "recipe",
    )
    ordering = ("pk",)
    empty_value_display = "-пусто-"


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "recipe",
    )
    ordering = ("pk",)
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
