import io
from collections import OrderedDict

from django.http.response import FileResponse
from fpdf import FPDF
from rest_framework import filters, status, viewsets
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     get_object_or_404)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (Favorite, Follow, Ingredient, Recipe, ShoppingList, Tag,
                     User)
from .permissions import IsAuthor
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeCreateUpdateSerializer,
                          RecipeForListSerializer, RecipeSerializer,
                          TagSerializer)


class Pagination(LimitOffsetPagination):
    default_limit = 10
    max_page_size = 100


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("-pub_date")
    serializer_class = RecipeSerializer
    pagination_class = Pagination
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "list": [AllowAny],
        "retriev": [AllowAny],
        "update": [IsAuthor],
        "destroy": [IsAuthor],
    }
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'tag',
    ]

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return RecipeCreateUpdateSerializer
        else:
            return RecipeSerializer


class Subscription(ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = Pagination

    def get_queryset(self):
        followings = User.objects.filter(
            following__user=self.request.user
        ).all()
        return followings


class SubscriptionCreateDestroy(GenericAPIView):
    def get(self, request, user_id):
        kwargs = {'context': self.get_serializer_context()}
        author = get_object_or_404(User, id=user_id)

        Follow.objects.create(user=request.user, author=author)
        serializer = FollowSerializer(instance=author, **kwargs)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscription = get_object_or_404(
            Follow, user=request.user, author_id=user_id
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteCreateDestroy(GenericAPIView):
    def get(self, request, recipe_id):
        kwargs = {'context': self.get_serializer_context()}
        recipe = get_object_or_404(Recipe, id=recipe_id)

        Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeForListSerializer(instance=recipe, **kwargs)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        favorite = get_object_or_404(
            Favorite, user=request.user, recipe_id=recipe_id
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListCreateDestroy(GenericAPIView):
    def get(self, request, recipe_id):
        kwargs = {'context': self.get_serializer_context()}
        recipe = get_object_or_404(Recipe, id=recipe_id)

        ShoppingList.objects.create(user=request.user, recipe=recipe)
        serializer = RecipeForListSerializer(instance=recipe, **kwargs)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        unit = get_object_or_404(
            ShoppingList, user=request.user, recipe_id=recipe_id
        )
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCart(GenericAPIView):

    def get_ingredients_list(self, recipes):
        ingredients = {}
        for recipe in recipes:
            for amount_ingredient in recipe.amounts_ingredients.all():
                name = f'{amount_ingredient.ingredient.name}'
                amount = amount_ingredient.amount
                measurement_unit = (
                    amount_ingredient.ingredient.measurement_unit
                )

                ingredient = ingredients.get(name, None)
                if ingredient:
                    ingredient['amount'] += amount
                else:
                    ingredients[name] = {
                        'amount': amount,
                        'measurement_unit': measurement_unit,
                    }

        return OrderedDict(
            sorted(ingredients.items(), key=lambda item: item[0])
        )

    def download_shopping_cart(self, request):
        recipes = request.user.shopping_list.all()
        ingredients_amounts = self.get_ingredients_list(recipes)
        pdf = FPDF()
        pdf.set_font('Arial', 'B', 14)
        pdf.add_page()
        for ingredient_name, amount_measurement in ingredients_amounts.items():
            text = (
                f'{ingredient_name} {amount_measurement["amount"]}'
                f' {amount_measurement["measurement_unit"]}'
            )
            pdf.cell(0, 10, txt=text, ln=1)

        string_file = pdf.output(dest='S')
        response = FileResponse(
            io.BytesIO(string_file.encode('latin1')),
            content_type='application/pdf',
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopong-list.pdf"'

        return response
