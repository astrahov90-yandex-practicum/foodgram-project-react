# Generated by Django 2.2.16 on 2022-03-15 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
            ],
            options={
                'ordering': ['ingredient'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=256, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, upload_to='posts/', verbose_name='Картинка')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('time', models.SmallIntegerField(verbose_name='Время приготовления (мин)')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Ключ')),
                ('color', models.CharField(max_length=7, unique=True, verbose_name='Цвет')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
