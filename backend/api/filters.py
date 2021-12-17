import django_filters

from .models import Favorite, Ingredient, Recipe, ShoppingList


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter()
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.ModelChoiceFilter(
        Favorite.objects.all()
    )
    is_in_shopping_cart = django_filters.ModelChoiceFilter(
        ShoppingList.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']
