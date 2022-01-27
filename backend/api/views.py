from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from djoser.views import UserViewSet


from .serializers import CustomUserSerializer, TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer, SubscribeAuthorSerializer
from .pagination import FoodgramPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from users.models import User, Follow
from recipes.models import Tag, Ingredient, Recipe, Favorite


class CustomUserViewSet(UserViewSet):
    pagination_class = FoodgramPagination

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        user = request.user

        if request.method == 'POST':
            if Follow.objects.filter(user=user, author=author).exists():
                return Response({"errors": "Вы уже подписаны на этого автора"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif author == user:
                return Response({"errors": "Нельзя подписываться на себя"},
                                status=status.HTTP_400_BAD_REQUEST)

            subscribtion = Follow.objects.create(user=user, author=author)
            serializer = SubscribeAuthorSerializer(subscribtion)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeAuthorSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)


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

    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        serializer = FavoriteRecipeSerializer(recipe)
        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response({"errors": "Рецепт уже добавлен в избранное"},
                                status=status.HTTP_400_BAD_REQUEST)

            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
