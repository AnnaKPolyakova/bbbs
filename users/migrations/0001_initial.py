# Generated by Django 3.2.3 on 2021-06-08 12:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Наставник', 'Наставник'), ('Модератор(региональный)', 'Модератор(региональный)'), ('Модератор(общий)', 'Модератор(общий)'), ('Администратор', 'Администратор')], default='Наставник', max_length=25, verbose_name='Роль')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='common.city', verbose_name='Город')),
                ('region', models.ManyToManyField(blank=True, related_name='region', related_query_name='region', to='common.City', verbose_name='Обслуживаемые города')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
            },
        ),
    ]
