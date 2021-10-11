from rest_framework import serializers

from .models import Ingredient, Recipe, Tag
from users.serializers import UserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        required=False,
        read_only=False,
    )
    ingredients = IngredientSerializer(
        many=True,
        required=False,
        read_only=False,
    )
    author = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = '__all__'
