# Generated by Django 3.2 on 2021-04-26 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etf', '0012_auto_20210426_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='name',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]