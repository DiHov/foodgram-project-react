from rest_framework import serializers

from .models import Ingredient, Recipe, Tag, IngredientAmount
from djoser.serializers import UserSerializer


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
        required=True,
        read_only=False,
    )
    ingredients = IngredientSerializer(
        many=True,
        required=True,
        read_only=False,
    )
    author = UserSerializer(
        read_only=True,
    )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = super.create(validated_data)
        for tag in tags_data:
            recipe.tags =       
        for ingredient in ingredients_data:
            IngredientAmount.objects.create(recipe=recipe, id=ingredient['id'], quantity=ingredient['amount'])
        return recipe

    class Meta:
        model = Recipe
        # fields = '__all__'
        exclude = ('pub_date',)
