from rest_framework import serializers

from recipes.models import (Favourites, Ingredient, IngredientsList, Recipe,
                            Shoplist, Tag)
from users.serializers import UserSerializer

from .fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели тегов.
    """
    class Meta:
        model = Tag

        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели ингридиентов.
    """
    class Meta:
        model = Ingredient

        fields = '__all__'


class IngredientListSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели списка ингредиентов.
    """

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all())
    name = serializers.StringRelatedField(
        source='ingredient.name',
        read_only=True)
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit',
        read_only=True)
    amount = serializers.FloatField()

    class Meta:
        model = IngredientsList

        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели рецептов.
    """

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientListSerializer(
        source='recipe_ingredients', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe

        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart',)

    def get_is_favorited(self, obj):
        """
        Метод возвращает признак избранного рецепта
        """
        if not self.context['request'].user.is_authenticated:
            return False
        user_recipes = self.context['request'].user.fav_recipes
        return user_recipes.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user.pk
        buyer = obj.shoplist_users.filter(user=user)
        return buyer.exists()


class RecipeSerializerPost(serializers.ModelSerializer):
    """
    Сериализатор модели рецептов. Операции записи.
    """

    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects)
    ingredients = IngredientListSerializer(
        source='recipe_ingredients',
        many=True)
    image = Base64ImageField(max_length=None, use_url=True,)

    class Meta:
        model = Recipe

        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        """
        Метод возвращает признак избранного рецепта
        """
        user_recipes = self.context['request'].user.fav_recipes
        return user_recipes.filter(recipe=obj).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            IngredientsList.objects.create(
                ingredient=ingredient['ingredient'],
                recipe=recipe,
                amount=ingredient['amount'])

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.set(tags)
        instance.recipe_ingredients.all().delete()
        for ingredient in ingredients:
            IngredientsList.objects.create(
                recipe=instance, ingredient=ingredient['ingredient'],
                amount=ingredient['amount'])
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели избранных рецептов.
    """

    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Favourites

        fields = ('user',
                  'recipe',)

    def get_recipes(self, obj):
        params = self.context['request'].query_params
        recipe_limit = params.get('recipe_limit') or 10
        recipes = obj.subscription.recipes.all()[:recipe_limit]
        return RecipeSerializer(recipes, many=True).data


class ShopSerializerPost(serializers.ModelSerializer):
    """
    Сериализатор модели избранных рецептов.
    Для операций добавления/удаления
    """

    class Meta:
        model = Shoplist

        fields = ('user',
                  'recipe',)
