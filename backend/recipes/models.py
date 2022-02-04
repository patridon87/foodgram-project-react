from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, verbose_name="Имя тэга"
    )
    color = models.CharField(
        max_length=7, unique=True, verbose_name="Цвет тэга"
    )
    slug = models.SlugField(
        max_length=200, unique=True
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name="Название ингредиента"
    )
    measurement_unit = models.CharField(
        max_length=200, verbose_name="Единицы измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        related_name="recipes",
        through="IngredientInRecipe",
    )
    tags = models.ManyToManyField(
        Tag, verbose_name="Тэги", related_name="recipes"
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name="recipes",
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name="Текст рецепта")
    image = models.ImageField(
        verbose_name="Картинка", upload_to="media/recipes/images/"
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления в минутах",
        validators=(
            MinValueValidator(
                1, message="Минимальное время приготовления - одна минута"
            ),
        ),
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User, related_name="recipe_subscribers", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="favorite_recipes", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Избранные рецепты"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite"
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, related_name="shopping_cart", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="shopping_cart", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_list"
            )
        ]


class IngredientInRecipe(models.Model):
    ordering = ["-id"]
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredient_to_recipe"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_to_recipe"
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество ингредиентов",
        validators=(
            MinValueValidator(1, "Минимальное количество ингредиентов - 1"),
        ),
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
