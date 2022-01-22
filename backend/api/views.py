from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

from .serializers import UserRegistrationSerializer, UserSerializer
from .pagination import FoodgramPagination
from .permissions import IsOwnerOrReadOnly
from users.models import User, Follow


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly, ]
    http_method_names = ["get", "post"]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserRegistrationSerializer

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class CreateUser(APIView):
#     def post(self, request, format=None):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.ecrrors, status=status.HTTP_400_BAD_REQUEST)