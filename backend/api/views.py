from django.shortcuts import render
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

from .serializers import CustomUserSerializer, TagSerializer, IngredientSerializer, RecipeSerializer
from .pagination import FoodgramPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from users.models import User, Follow
from recipes.models import Tag, Ingredient, Recipe


class UserViewSet(viewsets.ModelViewSet):
    pass


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get']
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get']
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    # def get_serializer_class(self):
    #     if self.request.method in SAFE_METHODS:
    #         return RecipeSerializer
    #     return RecipeCreateSerializer
