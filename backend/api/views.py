from django.db.models import Sum
from django_filters import rest_framework as filters
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import IngredientFilter, RecipeFilter
from .paginators import PageNumberPagination
from .permissions import IsRecipeOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerPost,
                          ShopSerializerPost, TagSerializer)
from .service import subscribe_delete, subscribe_post
from recipes.models import Ingredient, IngredientsRecipe, Recipe, Tag


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    Вьюсет модели категорий.
    Получение списка, получение элемента.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    Вьюсет модели ингредиентов.
    Получение списка, получение элемента.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter

    permission_classes = [AllowAny, ]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели рецептов. CRUD.
    """
    queryset = Recipe.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    permission_classes = [IsRecipeOwnerOrReadOnly]
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeSerializerPost
        return RecipeSerializer

    def get_queryset(self):
        return self.filterset_class.favorite_and_shopping_cart(self.request)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavouriteViewSet(APIView):
    """
    Класс избранных рецептов.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = PageNumberPagination

    def post(self, request, recipe_id):
        return subscribe_post(
            self,
            request,
            recipe_id,
            FavoriteSerializer,
            'fav_recipes',
            'Рецепт уже в избранном'
            )

    def delete(self, request, recipe_id):
        return subscribe_delete(
            self,
            request,
            recipe_id,
            'fav_recipes',
            'Рецепт не в избранном'
            )


class ShopViewSet(APIView):
    """
    Класс списка покупок.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShopSerializerPost

    def get(self, request):
        recipes_id = request.user.shoplist_recipes.values_list('recipe__id')
        ingredients = IngredientsRecipe.objects.filter(recipe__in=recipes_id)
        ingredients = ingredients.values(
            'ingredient',
            'ingredient__name',
            'ingredient__measurement_unit'
            )
        ingredients = ingredients.annotate(sum_amount=Sum('amount'))
        data = []
        data.append('Список ваших покупок')
        data.append('Ингредиент (ед.) - кол-во')
        for ing in ingredients:
            ing_name = ing.get("ingredient__name")
            ing_unit = ing.get("ingredient__measurement_unit")
            data.append(f'• {ing_name} ({ing_unit}) - {ing.get("sum_amount")}')
        return Response(
            '\r\n'.join(data),
            status=status.HTTP_200_OK,
            content_type='text/plain')

    def post(self, request, recipe_id):
        return subscribe_post(
            self,
            request,
            recipe_id,
            ShopSerializerPost,
            'shoplist_recipes',
            'Рецепт уже в корзине'
            )

    def delete(self, request, recipe_id):
        return subscribe_delete(
            self,
            request,
            recipe_id,
            'shoplist_recipes',
            'Рецепт не в корзине'
            )
