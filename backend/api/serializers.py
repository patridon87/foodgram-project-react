from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User, Follow
from recipes.models import Tag, Ingredient, Recipe


class UserRegistrationSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user == obj:
            return False
        return (
                user.is_authenticated
                and obj.following.filter(user=user).exists()
                )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit'
        )


class IngredientToCreateRecipeSerializer(serializers.ModelField):
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit", "amount")


class IngredientInRecipeSerializer(serializers.ModelField):
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = Ingredient
        fields = ("id", "amount")


class TagToCreateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id",)


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientToCreateRecipeSerializer(many=True, required=True)
    tags = TagToCreateRecipeSerializer(many=True, required=True)
    image = Base64ImageField()
    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientInRecipeSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
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
            "cooking_time"
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return (
                user.is_authenticated
                and obj.faworited_recipes.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return (
                user.is_authenticated
                and obj.in_shopping_cart.filter(user=user).exists()
        )

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
