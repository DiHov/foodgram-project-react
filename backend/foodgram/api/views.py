from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from .models import Ingredient, Recipe, Tag
from .permissions import IsAuthor
from .serializers import (IngredientSerializer,
                          RecipetSerializer, TagSerializer)


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
    queryset = Recipe.objects.all()
    serializer_class = RecipetSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'tag',
    ]

    # def get_serializer_class(self):
    #     if self.action in ("list", "retrieve"):
    #         return RecipetSerializer
    #     return RecipeCreateUpdateSerializer

    # def get_permissions(self):
    #     if self.action in ('list', 'retrieve'):
    #         permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [IsAuthor]
    #     return [permission() for permission in permission_classes]
