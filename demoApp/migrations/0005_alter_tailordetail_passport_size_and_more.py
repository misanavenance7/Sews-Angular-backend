# Generated by Django 4.2.16 on 2024-10-10 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("demoApp", "0004_tailordetail_groups_tailordetail_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tailordetail",
            name="passport_size",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="tailorproduct",
            name="product_image",
            field=models.CharField(max_length=255),
        ),
    ]
