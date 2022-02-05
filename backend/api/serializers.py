from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Follow, User


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password"
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email",
                  "id",
                  "username",
                  "first_name",
                  "last_name",
                  "is_subscribed"
                  )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user == obj:
            return False
        return (user.is_authenticated
                and obj.following.filter(user=user).exists())


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class MiniRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscribeAuthorSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        extra_kwargs = {
            "email": {"read_only": True},
            "id": {"read_only": True},
            "username": {"read_only": True},
            "first_name": {"read_only": True},
            "lastname": {"read_only": True},
        }

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit", None)
        if limit is None:
            recipes = Recipe.objects.filter(author=obj)
        else:
            recipes = Recipe.objects.filter(author=obj)[: int(limit)]
        return MiniRecipeSerializer(recipes, many=True, read_only=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context.get("user")
        return Follow.objects.filter(user=user, author=obj).exists()


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source="ingredient_to_recipe", many=True, read_only=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        amount = data["amount"]
        if isinstance(amount, int):
            return data
        raise serializers.ValidationError("Количество ингредиента должно быть"
                                          " числом")

    def create(self, validated_data):
        author = self.context["request"].user
        tags = self.initial_data.get("tags")
        ingredients = self.initial_data.get("ingredients")
        recipe = Recipe.objects.create(**validated_data, author=author)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, pk=ingredient["id"]
            )

            IngredientInRecipe.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient["amount"],
            )
            recipe.ingredients.add(current_ingredient)
        return recipe

    def update(self, instance, validated_data):
        if "tags" in self.initial_data:
            instance.tags.clear()
            tags = self.initial_data.get("tags")
            for tag in tags:
                instance.tags.add(tag)
        if "ingredients" in self.initial_data:
            instance.ingredients.clear()
            IngredientInRecipe.objects.filter(recipe=instance).delete()
            ingredients = self.initial_data.get("ingredients")
            for ingredient in ingredients:
                current_ingredient = get_object_or_404(
                    Ingredient, pk=ingredient["id"]
                )

                IngredientInRecipe.objects.create(
                    ingredient=current_ingredient,
                    recipe=instance,
                    amount=ingredient["amount"],
                )
                instance.ingredients.add(current_ingredient)

        super().update(instance, validated_data)

        return instance

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        return (user.is_authenticated
                and obj.favorite_recipes.filter(user=user).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        return (user.is_authenticated
                and obj.shopping_cart.filter(user=user).exists())
