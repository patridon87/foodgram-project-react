from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

from .serializers import CustomUserSerializer, TagSerializer, IngredientSerializer
from .pagination import FoodgramPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from users.models import User, Follow
from recipes.models import Tag, Ingredient


class UserViewSet(viewsets.ModelViewSet):
    pass
    # queryset = User.objects.all()
    # permission_classes = [IsOwnerOrReadOnly, ]
    # http_method_names = ["get", "post"]
    #
    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return UserSerializer
    #     return UserRegistrationSerializer
    #
    # @action(
    #     detail=False,
    #     methods=["get"],
    #     permission_classes=[permissions.IsAuthenticated]
    # )
    # def me(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


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
