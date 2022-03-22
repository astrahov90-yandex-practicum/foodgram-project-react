from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    IngredientsRecipe,
    Recipe,
    Shopcart,
    Tag
    )


class CustomIngredientsListAdmin(admin.TabularInline):
    model = IngredientsRecipe
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


class ShopcartAdmin(admin.ModelAdmin):
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

admin.site.register(Favorite, FavoriteAdmin)

admin.site.register(Shopcart, ShopcartAdmin)
