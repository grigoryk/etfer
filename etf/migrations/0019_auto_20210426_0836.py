# Generated by Django 3.2 on 2021-04-26 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etf', '0018_auto_20210426_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='ticker',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
