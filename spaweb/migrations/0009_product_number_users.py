# Generated by Django 3.1.2 on 2020-11-20 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaweb', '0008_auto_20201116_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='number_users',
            field=models.IntegerField(default=1, verbose_name='количество пользователей'),
        ),
    ]