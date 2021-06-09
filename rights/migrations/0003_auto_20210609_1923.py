# Generated by Django 3.2.3 on 2021-06-09 19:23

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rights', '0002_remove_right_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='RightTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Права детей - Тег',
                'verbose_name_plural': 'Права детей — Теги',
            },
        ),
        migrations.RemoveField(
            model_name='right',
            name='image',
        ),
        migrations.AddField(
            model_name='right',
            name='imageUrl',
            field=models.ImageField(blank=True, help_text='Добавить фото', upload_to='rights/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='right',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', max_length=18, verbose_name='Цвет обложки на странице'),
        ),
        migrations.AlterField(
            model_name='right',
            name='description',
            field=models.CharField(max_length=500, verbose_name='Описание права ребенка'),
        ),
        migrations.AlterField(
            model_name='right',
            name='text',
            field=models.TextField(verbose_name='Основной текст права ребенка'),
        ),
        migrations.AlterField(
            model_name='right',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Право ребенка'),
        ),
        migrations.AddField(
            model_name='right',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tags', to='rights.RightTag'),
        ),
    ]
