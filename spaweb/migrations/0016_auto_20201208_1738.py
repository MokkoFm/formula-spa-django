# Generated by Django 3.1.2 on 2020-12-08 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spaweb', '0015_remove_orderitem_order_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='spaweb.customer', verbose_name='Покупатель'),
        ),
    ]
