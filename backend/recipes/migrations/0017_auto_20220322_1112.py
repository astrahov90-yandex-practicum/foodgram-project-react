# Generated by Django 2.2.16 on 2022-03-22 08:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0016_auto_20220322_1110'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favourites',
            new_name='Favorite',
        ),
        migrations.RenameModel(
            old_name='Shoplist',
            new_name='Shopcart',
        ),
    ]
