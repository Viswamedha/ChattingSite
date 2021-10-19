# Generated by Django 3.2.7 on 2021-09-25 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0002_auto_20210925_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='capital',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Capital'),
        ),
        migrations.AlterField(
            model_name='country',
            name='content',
            field=models.TextField(blank=True, max_length=3000, null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='country',
            name='currency',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='country',
            name='flag',
            field=models.ImageField(blank=True, null=True, upload_to='flags/', verbose_name='Flag'),
        ),
        migrations.AlterField(
            model_name='country',
            name='key_landmarks',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Key Landmarks'),
        ),
        migrations.AlterField(
            model_name='country',
            name='location',
            field=models.URLField(blank=True, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='country',
            name='national_animal',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='National Animal(s)'),
        ),
        migrations.AlterField(
            model_name='country',
            name='national_language',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='National Language'),
        ),
        migrations.AlterField(
            model_name='country',
            name='national_sport',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='National Sport(s)'),
        ),
        migrations.AlterField(
            model_name='country',
            name='other_large_cities',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Other Large Cities'),
        ),
        migrations.AlterField(
            model_name='country',
            name='population',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Population'),
        ),
        migrations.AlterField(
            model_name='country',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]