# Generated by Django 3.1.3 on 2020-11-20 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spaweb', '0009_product_number_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='number_users',
        ),
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_products', to='spaweb.productcategory', verbose_name='категория'),
        ),
    ]
