# Generated by Django 4.1.1 on 2022-11-05 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0003_alter_order_end_at_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='end_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
