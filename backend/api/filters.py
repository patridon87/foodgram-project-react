from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (
    AllValuesFilter, AllValuesMultipleFilter, BooleanFilter
)
from django_filters.widgets import BooleanWidget
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = BooleanFilter(method="filter_is_in_shopping_cart")
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    author = AllValuesFilter(field_name="author__id")

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return Recipe.objects.filter(favorite_recipes__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return Recipe.objects.filter(shopping_cart__user=user)
        return queryset

    class Meta:
        model = Recipe
        fields = ["tags__slug", "author__id"]


class IngredientFilter(SearchFilter):
    search_param = "name"
