from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavouriteViewSet, IngredientViewSet, RecipeViewSet,
                    ShopViewSet, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(
    'tags',
    TagViewSet,
    basename='tags')

router.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients')

router.register('recipes',
                RecipeViewSet,
                basename='recipes')


urlpatterns = [
    path(r'recipes/<recipe_id>/favorite/', FavouriteViewSet.as_view()),
    path(r'recipes/download_shopping_cart/', ShopViewSet.as_view()),
    path(r'recipes/<recipe_id>/shopping_cart/', ShopViewSet.as_view()),
    path('', include(router.urls)),
]
