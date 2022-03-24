from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import IngredientsRecipe, Recipe
from . import serializers


def fill_recipe(instance, ingredients, tags):
    """
    Служебная процедура заполнения ингредиентов в рецепте.
    """

    instance.tags.set(tags)
    instance.recipe_ingredients.all().delete()

    for ingredient in ingredients:
        IngredientsRecipe.objects.create(
            ingredient=ingredient['ingredient'],
            recipe=instance,
            amount=ingredient['amount'])

    return instance


def subscribe_post(self, request, recipe_id, serializer, inner_tag, error_msg):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if inner_tag == 'shoplist_recipes':
        if request.user.shoplist_recipes.filter(recipe=recipe).exists():
            raise ValidationError(error_msg)
    else:
        if request.user.fav_recipes.filter(recipe=recipe).exists():
            raise ValidationError(error_msg)
    data = {'user': request.user.pk,
            'recipe': recipe.pk}
    serializer = serializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user, recipe=recipe)
        model = serializers.RecipeSerializerShort(instance=recipe)
        return Response(data=model.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def subscribe_delete(self, request, recipe_id, inner_tag, error_msg):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if inner_tag == 'shoplist_recipes':
        instance = request.user.shoplist_recipes.filter(recipe=recipe)
    else:
        instance = request.user.fav_recipes.filter(recipe=recipe)

    if not instance.exists():
        return Response(data=error_msg,
                        status=status.HTTP_400_BAD_REQUEST)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
