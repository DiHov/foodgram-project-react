from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    measurement_unit = models.CharField(max_length=20)


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    slug = models.SlugField()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Автор',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(max_length=100)
    # image = models.ImageField()
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField(default=0)
