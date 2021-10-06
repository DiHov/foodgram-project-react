from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'quantity', 'dimension')
        model = Ingredient
        lookup_field = 'name'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'hex_code', 'slug')
        model = Tag
        lookup_field = 'name'


class RecipetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'author',
            'name',
            'description',
            'ingredients',
            'tag',
            'cooking_time'
        )
        model = Recipe
        lookup_field = 'name'
