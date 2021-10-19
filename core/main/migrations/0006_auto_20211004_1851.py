# Generated by Django 3.2.7 on 2021-10-04 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210924_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='groups_created', to='main.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='groups_owned', to='main.user'),
            preserve_default=False,
        ),
    ]
