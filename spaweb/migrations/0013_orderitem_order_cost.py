# Generated by Django 3.1.2 on 2020-12-03 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaweb', '0012_auto_20201130_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='order_cost',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='стоимость'),
        ),
    ]
