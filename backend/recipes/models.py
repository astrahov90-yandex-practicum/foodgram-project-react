from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """
    Модель данных тега.
    """
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200,
        unique=True)
    slug = models.SlugField(
        verbose_name='Ключ',
        max_length=200,
        unique=True)
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель данных ингредиента.
    """
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель данных рецептов.
    """
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги')

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes')

    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        db_index=True)

    image = models.ImageField(
        'Картинка',
        upload_to='media/',
        blank=True)

    text = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True)

    cooking_time = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления (мин)',
        blank=False,
        null=False
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления рецепта',
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe'
        )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        help_text='Содержит рецепт')

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_in_recipe',
        verbose_name='Ингредиент',
        help_text='Содержит ингредиент')

    amount = models.FloatField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество',
        help_text='Содержит количество ингредиентов')

    class Meta:
        ordering = ['ingredient']
        unique_together = ('recipe', 'ingredient',)

    def __str__(self) -> str:
        measurement_unit = self.ingredient.measurement_unit
        return f'{self.ingredient.name} ({self.amount}) - {measurement_unit}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fav_recipes',
        verbose_name='Хозяин списка избранного',
        help_text='Содержит хозяина списка избранного')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='fav_users',
        verbose_name='Рецепт',
        help_text='Содержит рецепт')

    class Meta:
        ordering = ['-recipe__created_date']
        unique_together = ('user', 'recipe',)

    def __str__(self) -> str:
        return ', '.join([r.name for r in self.recipe])


class Shopcart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoplist_recipes',
        verbose_name='Хозяин списка покупок',
        help_text='Содержит хозяина списка покупок')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoplist_users',
        verbose_name='Рецепт',
        help_text='Содержит рецепт')

    class Meta:
        ordering = ['-recipe__created_date']
        unique_together = ('user', 'recipe',)

    def __str__(self) -> str:
        return ', '.join([r.name for r in self.recipe])
