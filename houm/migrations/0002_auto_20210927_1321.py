# Generated by Django 3.2.7 on 2021-09-27 18:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('houm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='dateModified',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
