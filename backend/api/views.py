from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Follow, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import FoodgramPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (MiniRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, SubscribeAuthorSerializer,
                          TagSerializer)


class CustomUserViewSet(UserViewSet):
    pagination_class = FoodgramPagination

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        user = request.user

        if request.method == "POST":
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {"errors": "Вы уже подписаны на этого автора"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif author == user:
                return Response(
                    {"errors": "Нельзя подписываться на себя"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Follow.objects.create(user=user, author=author)
            serializer = SubscribeAuthorSerializer(
                author,
                context={"request": request, "author": author, "user": user})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeAuthorSerializer(
            page, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ("^name",)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = RecipeSerializer
    pagination_class = FoodgramPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    http_method_names = ["get", "post", "patch", "delete"]

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        serializer = MiniRecipeSerializer(recipe)
        if request.method == "POST":
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже добавлен в избранное"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == "POST":
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {"errors": "Рецепт уже добавлен в список покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(
                user=user, recipe=recipe
            )
            serializer = MiniRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_list = {}
        user = request.user
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=user
        ).values("ingredient__name", "ingredient__measurement_unit", "amount")

        for ingredient in ingredients:
            name = ingredient["ingredient__name"]
            amount = ingredient["amount"]
            measurement_unit = ingredient["ingredient__measurement_unit"]
            if name in shopping_list:
                shopping_list[name]["amount"] += amount
            else:
                shopping_list[name] = {
                    "amount": amount,
                    "measurement_unit": measurement_unit,
                }

        response = HttpResponse(content_type="text/plain")
        response["Content_Disposition"] = (
            "attachment; filename=shopping_list.txt"
        )

        for key, value in shopping_list.items():
            line = f'{key} {value["amount"]} {value["measurement_unit"]}\n'
            response.write(line)
        return response
