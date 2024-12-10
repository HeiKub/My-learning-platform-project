# Generated by Django 5.0.6 on 2024-09-24 13:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                (
                    "material_types",
                    models.CharField(
                        choices=[
                            ("file", "File"),
                            ("video", "Video"),
                            ("link", "Link"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "content_file",
                    models.FileField(blank=True, null=True, upload_to="materials/"),
                ),
                ("video_url", models.URLField(blank=True, null=True)),
                ("link_url", models.URLField(blank=True, null=True)),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "topic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="topics.topic"
                    ),
                ),
            ],
        ),
    ]
