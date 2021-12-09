from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteCreateDestroy, IngredientViewSet, RecipeViewSet,
                    ShoppingCart, ShoppingListCreateDestroy, Subscription,
                    SubscriptionCreateDestroy, TagViewSet)

router_v1 = DefaultRouter()

router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet)
router_v1.register('tags', TagViewSet)


urlpatterns = [
    path(
        '', include(router_v1.urls),
    ),
    path(
        'users/subscriptions/',
        Subscription.as_view(),
        name='subscriptions-list',
    ),
    re_path(
        r'users/(?P<user_id>\d+)/subscribe/',
        SubscriptionCreateDestroy.as_view(),
        name='subscriptions-detail',
    ),
    re_path(
        r'recipes/(?P<recipe_id>\d+)/favorite/',
        FavoriteCreateDestroy.as_view(),
        name='favorite',
    ),
    re_path(
        r'recipes/(?P<recipe_id>\d+)/shopping_cart/',
        ShoppingListCreateDestroy.as_view(),
        name='shopping-list',
    ),
    path(
        'recipes/download_shopping_cart/',
        ShoppingCart.as_view(),
        name='download-shopping-list',
    ),
]
