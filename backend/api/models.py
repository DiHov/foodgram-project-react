from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=20,
        verbose_name='Цвет',
    )
    slug = models.CharField(
        max_length=20,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=100,
    )
    image = models.ImageField(
        upload_to=r"recipes/%Y/%m/%d/",
        verbose_name="Изображение",
        unique=False,
        blank=False,
        null=False,
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'

    def __str__(self):
        return f'{self.name}, {self.author.username}'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='amount_ingredients',
    )
    amount = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Количество',
    )

    def __str__(self):
        return self.ingredient.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow')]

    def __str__(self):
        return f'{self.author.get_username()}:{self.user.get_username()}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites_recipes',
        blank=True,
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorte')]

    def __str__(self):
        return f'{self.user.username}:{self.recipe.name}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        blank=True,
        null=True,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shoppinglist')]

    def __str__(self):
        return f'{self.user.username}:{self.recipe.name}'
