# Generated by Django 3.2 on 2021-04-26 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etf', '0008_rename_assetinvestment_assetinetf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinetf',
            name='market_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='assetinetf',
            name='notional_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='assetinetf',
            name='shares',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='assetinetf',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
