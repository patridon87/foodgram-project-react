# Generated by Django 2.2.19 on 2022-01-24 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220124_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_to_recipe', to='recipes.Ingredient'),
        ),
    ]