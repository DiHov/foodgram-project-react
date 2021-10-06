from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router_v1 = DefaultRouter()

router_v1.register('ingridient', IngredientViewSet)
router_v1.register('recipe', RecipeViewSet)
router_v1.register('tag', TagViewSet)


urlpatterns = [
    path(
        'v1/',
        include(router_v1.urls),
    ),
]
