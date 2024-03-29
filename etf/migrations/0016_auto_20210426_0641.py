# Generated by Django 3.2 on 2021-04-26 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etf', '0015_rawdata_overrides'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='rawdata',
            name='overrides',
            field=models.TextField(blank=True, default='{\n    "asset":{},\n    "etf": {}\n}', null=True),
        ),
    ]
