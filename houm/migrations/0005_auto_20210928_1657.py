# Generated by Django 3.2.7 on 2021-09-28 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houm', '0004_position_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='distance',
            field=models.DecimalField(decimal_places=9, default=False, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='speed',
            field=models.DecimalField(decimal_places=9, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='position',
            name='visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='position',
            name='dateModified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='latitude',
            field=models.DecimalField(decimal_places=9, max_digits=9),
        ),
        migrations.AlterField(
            model_name='position',
            name='longitude',
            field=models.DecimalField(decimal_places=9, max_digits=9),
        ),
    ]