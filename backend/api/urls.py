from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, TagViewSet, IngredientViewSet, RecipeViewSet


router_v1 = SimpleRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),

]
