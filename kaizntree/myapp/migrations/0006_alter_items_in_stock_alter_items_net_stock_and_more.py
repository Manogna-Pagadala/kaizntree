# Generated by Django 5.0.2 on 2024-02-12 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_category_alter_items_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='in_stock',
            field=models.BooleanField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='net_stock',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='quantity_sold_last_month',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='quantity_sold_this_month',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='items',
            name='tags',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
