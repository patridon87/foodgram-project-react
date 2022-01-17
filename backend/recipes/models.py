from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Имя тэга"
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="Цвет тэга"
    )
    slug = models.SlugField(max_length=200, unique=True)


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name="Единицы измерения"
    )


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта",

    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        related_name="recipes"
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тэги",
        related_name="recipes"
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="recipes",
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name="Текст рецепта"
    )
    cooking_time = models.SmallIntegerField(
        verbose_name="Время приготовления в минутах",
        validators=MinValueValidator(
            1,
            message="Минимальное время приготовления - одна минута"
        )
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name="recipe_subscribers",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorite_recipes",
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"],
                                    name="unique_favorite")
        ]


class ShoppingList(models.Model):
    pass
