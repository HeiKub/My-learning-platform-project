# Generated by Django 5.0.6 on 2024-09-25 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("topics", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="material",
            old_name="material_types",
            new_name="material_type",
        ),
    ]
