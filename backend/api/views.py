import io
from collections import OrderedDict

from django.http.response import FileResponse
from fpdf import FPDF
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     get_object_or_404)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (Favorite, Follow, Ingredient, Recipe, ShoppingList, Tag,
                     User)
from .permissions import IsAuthor
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeCreateUpdateSerializer,
                          RecipeForListSerializer, RecipeSerializer,
                          TagSerializer)
from .paginatons import Pagination


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
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthor],
        'destroy': [IsAuthor],
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

    def create(self, request, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        create_serializer = RecipeCreateUpdateSerializer(
            data=request.data, *args, **kwargs
        )
        create_serializer.is_valid(raise_exception=True)
        recipe = create_serializer.save(author=self.request.user)

        retrieve_serializer = RecipeSerializer(
            instance=recipe, *args, **kwargs
        )
        headers = self.get_success_headers(retrieve_serializer.data)
        return Response(
            retrieve_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs.pop('pk')

        instance = self.get_object()
        update_serializer = RecipeCreateUpdateSerializer(
            instance,
            data=request.data,
            partial=partial,
        )
        update_serializer.is_valid(raise_exception=True)
        instance = update_serializer.save(author=self.request.user)
        retrieve_serializer = RecipeSerializer(
            instance=instance, **kwargs
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(retrieve_serializer.data)

    def get_ingredients_list(self, recipes):
        ingredients = {}
        for recipe in recipes:
            for amount_ingredient in recipe.amount_ingredients.all():
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

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        shopping_list = request.user.shopping_user.all()
        recipes = []
        for item in shopping_list:
            recipes.append(item.recipe)
        print(recipes)
        ingredients_amounts = self.get_ingredients_list(recipes)
        pdf = FPDF()
        pdf.add_font(
            "DejaVu", "", "./api/fonts/DejaVuSansCondensed.ttf", uni=True
        )
        pdf.set_font("DejaVu", "", 14)
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

        Follow.objects.get_or_create(user=request.user, author=author)
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

        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
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

        ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
        serializer = RecipeForListSerializer(instance=recipe, **kwargs)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        unit = get_object_or_404(
            ShoppingList, user=request.user, recipe_id=recipe_id
        )
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
