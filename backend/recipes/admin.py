from django.contrib import admin

from .models import (Favourites, Ingredient, IngredientsList, Recipe, Shoplist,
                     Tag)


class CustomIngredientsListAdmin(admin.TabularInline):
    model = IngredientsList
    extra = 1


class CustomRecipeAdmin(admin.ModelAdmin):
    inlines = (CustomIngredientsListAdmin,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    fieldsets = [
        (None, {'fields': ['user', 'recipe']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'fields': [
                    'user',
                    'recipe',
                ]
            },
        ),
    ]


class ShopAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    fieldsets = [
        (None, {'fields': ['user', 'recipe']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'fields': [
                    'user',
                    'recipe',
                ]
            },
        ),
    ]


admin.site.register(Ingredient)

admin.site.register(Recipe, CustomRecipeAdmin)

admin.site.register(Tag)

admin.site.register(Favourites, FavoriteAdmin)

admin.site.register(Shoplist, ShopAdmin)
