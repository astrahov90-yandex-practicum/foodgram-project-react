# Generated by Django 2.2.16 on 2022-03-22 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20220322_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.AlterUniqueTogether(
            name='ingredientslist',
            unique_together={('recipe', 'ingredient')},
        ),
    ]
