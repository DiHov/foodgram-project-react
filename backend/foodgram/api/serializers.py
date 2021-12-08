from django.db import transaction
from django.shortcuts import get_list_or_404, get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import CustomUserSerializer

from .models import Ingredient, IngredientAmount, Recipe, Tag, User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'amount', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
    )
    ingredients = IngredientAmountSerializer(
        many=True,
        source='amount_ingredients',
    )
    author = CustomUserSerializer(
        read_only=True,
        required=False
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            # 'image',
            'name',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, current_recipe):
        user = self.context['request'].user
        return current_recipe.in_favorites.filter(
            user_id=user.pk
        ).exists()

    def get_is_in_shopping_cart(self, current_recipe):
        user = self.context['request'].user
        return current_recipe.shopping_list.filter(user_id=user.pk).exists()


class RecipeCreateUpdateSerializer(RecipeSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        with transaction.atomic():
            tags_ids = validated_data['tags']
            tags = get_list_or_404(Tag, pk__in=tags_ids)

            recipe = Recipe.objects.create(
                author=self.context['request'].user,
                name=validated_data['name'],
                # image=validated_data['image'],
                text=validated_data['text'],
                cooking_time=validated_data['cooking_time'],
            )

            amounts_instance = []
            for ingredient_data in validated_data['ingredients']:
                print(validated_data)
                amount = ingredient_data['amount']
                amounts_instance.append(
                    IngredientAmount(
                        amount=amount,
                        recipe=recipe,
                        ingredient=Ingredient.objects.get(
                            pk=ingredient_data['id']
                        ),
                    )
                )
            IngredientAmount.objects.bulk_create(amounts_instance)
            recipe.tags.set(tags)

        return recipe

    def update(self, recipe, validated_data):
        with transaction.atomic():
            tags_ids = validated_data.pop('tags', None)
            if tags_ids:
                tags = get_list_or_404(Tag, pk__in=tags_ids)
                recipe.tags.set(tags)

            ingredients = validated_data.pop('ingredients', None)
            if ingredients:
                recipe.amount_ingredients.all().delete()
                new_amounts_intstance = []
                for ingredient in ingredients:
                    id, amount = ingredient.values()
                    new_amounts_intstance.append(
                        IngredientAmount(
                            amount=amount,
                            recipe=recipe,
                            ingredient=get_object_or_404(
                                Ingredient, pk=id
                            ),
                        )
                    )
                IngredientAmount.objects.bulk_create(new_amounts_intstance)

            for attribute, value in validated_data.items():
                setattr(recipe, attribute, value)
            recipe.save()
        return recipe


class RecipeForListSerializer(serializers.ModelSerializer):
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            # 'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeForListSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, author):
        request = self.context.get('request')
        if request:
            requested_user = request.user
        return author.following.filter(
            user=requested_user
        ).exists()

    def get_recipes_count(self, author):
        return author.recipes.count()
