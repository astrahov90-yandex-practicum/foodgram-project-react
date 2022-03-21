from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from recipes.models import Ingredient, IngredientsList, Recipe, Tag

from .filters import IngredientFilter, RecipeFilter
from .paginators import PageNumberPagination
from .permissions import IsRecipeOwnerOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeSerializerPost,
                          ShopSerializerPost, TagSerializer)


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
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user.fav_recipes.filter(recipe=recipe).exists():
            raise ValidationError('Рецепт уже в избранном')
        data = {'user': request.user.pk,
                'recipe': recipe.pk}
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        instance = request.user.fav_recipes.filter(recipe=recipe)
        if not instance.exists():
            return Response(data='Рецепт не в избранном',
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopViewSet(APIView):
    """
    Класс списка покупок.
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShopSerializerPost

    def get(self, request):
        recipes = request.user.shoplist_recipes.select_related('recipe').all()
        recipes = [recipe.recipe for recipe in recipes]
        ingredients = IngredientsList.objects.filter(recipe__in=recipes)
        ingredients_aggr = ingredients.annotate(sum_amount=Sum('amount'))
        data = []
        data.append('Список ваших покупок')
        data.append('Ингредиент (ед.) - кол-во')
        for ing in ingredients_aggr:
            ing_name = ing.ingredient.name
            ing_init = ing.ingredient.measurement_unit
            data.append(f'• {ing_name} ({ing_init}) - {ing.sum_amount}')
        return Response(
            '\r\n'.join(data),
            status=status.HTTP_200_OK,
            content_type='text/plain')

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user.shoplist_recipes.filter(recipe=recipe).exists():
            raise ValidationError('Рецепт уже в корзине')
        data = {'user': request.user.pk,
                'recipe': recipe.pk}
        serializer = ShopSerializerPost(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        instance = request.user.shoplist_recipes.filter(recipe=recipe)
        if not instance.exists():
            return Response(data='Рецепт не в корзине',
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
