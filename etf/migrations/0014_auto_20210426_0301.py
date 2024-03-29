# Generated by Django 3.2 on 2021-04-26 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etf', '0013_portfolio_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetinetf',
            name='market_value',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='assetinetf',
            name='notional_value',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='assetinetf',
            name='shares',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='assetinetf',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='etf',
            name='expense_ratio',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='etfinportfolio',
            name='weight',
            field=models.DecimalField(decimal_places=4, max_digits=5),
        ),
    ]
