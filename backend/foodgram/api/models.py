from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField
    dimension = models.CharField(max_length=20)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=20)
    slug = models.SlugField()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='???',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField
