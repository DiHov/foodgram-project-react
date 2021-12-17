import django_filters
from django.contrib.auth import get_user_model

from .models import Ingredient, Recipe

User = get_user_model()


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(queryset=User.objects.all())
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.CharFilter(method='get_is_favorited')
    is_in_shopping_cart = django_filters.CharFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def get_is_favorited(self, queryset, name, value):
        if value is True:
            return queryset.filter(favorites_recipes=self.request.user)
        return None

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value is True:
            return queryset.filter(shopping_user=self.request.user)
        return None


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name']
