# Generated by Django 3.1.3 on 2023-03-15 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaweb', '0019_auto_20221203_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(blank=True, null=True, verbose_name='Промокод'),
        ),
    ]
