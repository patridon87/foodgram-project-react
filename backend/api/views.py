from django.shortcuts import render
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer
from users.models import User, Follow


# class CreateUser(APIView):
#     def post(self, request, format=None):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)