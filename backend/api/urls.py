from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet


router_v1 = SimpleRouter()

router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [

    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
