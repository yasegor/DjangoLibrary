# Generated by Django 4.1.1 on 2022-11-05 19:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0004_alter_order_end_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='end_at',
            field=models.DateField(),
        ),
    ]
