# Generated by Django 3.2.7 on 2021-09-24 11:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210917_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blocked',
            field=models.ManyToManyField(blank=True, related_name='_main_user_blocked_+', to=settings.AUTH_USER_MODEL, verbose_name='Blocked'),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='_main_user_following_+', to=settings.AUTH_USER_MODEL, verbose_name='Following'),
        ),
        migrations.AlterField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_main_user_friends_+', to=settings.AUTH_USER_MODEL, verbose_name='Friends'),
        ),
    ]