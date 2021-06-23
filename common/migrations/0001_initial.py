# Generated by Django 3.2.4 on 2021-06-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите город', max_length=30, unique=True, verbose_name='Город')),
                ('isPrimary', models.BooleanField(default=False, help_text='Укажите, если город должен иметь приоритетный вывод', verbose_name='Приоритет вывода')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
    ]
