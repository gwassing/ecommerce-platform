# Generated by Django 5.0.7 on 2024-09-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_name_product_item_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('SHOES', 'Shoes'), ('CLOTHING', 'Clothing'), ('ACCESSORIES', 'Accessories')], max_length=50),
        ),
    ]
