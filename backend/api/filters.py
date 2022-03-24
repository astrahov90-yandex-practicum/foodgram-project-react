from django_filters import rest_framework as filters
from django.db.models import Q

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    @staticmethod
    def favorite_and_shopping_cart(request):
        user = request.user
        if user.is_anonymous:
            return Recipe.objects.all()
        fav_param_value = request.query_params.get('is_favorited')
        shop_param_value = request.query_params.get(
            'is_in_shopping_cart'
        )

        URLS_VALID_VALUE_PARAMS = {'True': ['true', '1', 'True']}

        is_favorite = (fav_param_value in
                       URLS_VALID_VALUE_PARAMS['True'])
        in_shop_cart = (shop_param_value in
                        URLS_VALID_VALUE_PARAMS['True'])
        if is_favorite and in_shop_cart:
            recipes_id_shop = user.shoplist_recipes.values_list('recipe__id')
            recipes_id_fav = user.fav_recipes.values_list('recipe__id')
            criterion1 = Q(pk__in=recipes_id_shop)
            criterion2 = Q(pk__in=recipes_id_fav)
            return Recipe.objects.filter(criterion1 & criterion2)
        elif in_shop_cart:
            recipes_id = user.shoplist_recipes.values_list('recipe__id')
            return Recipe.objects.filter(pk__in=recipes_id)
        elif is_favorite:
            recipes_id = user.fav_recipes.values_list('recipe__id')
            return Recipe.objects.filter(pk__in=recipes_id)
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
