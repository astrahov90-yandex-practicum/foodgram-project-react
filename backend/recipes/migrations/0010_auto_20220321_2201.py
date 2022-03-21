# Generated by Django 2.2.16 on 2022-03-21 19:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20220321_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='recipe',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата добавления рецепта'),
            preserve_default=False,
        ),
    ]
