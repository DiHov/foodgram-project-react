from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
