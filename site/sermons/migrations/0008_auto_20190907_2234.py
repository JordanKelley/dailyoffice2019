# Generated by Django 2.2.4 on 2019-09-07 22:34

import address.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [("address", "0002_auto_20160213_1726"), ("sermons", "0007_auto_20190828_0153")]

    operations = [
        migrations.AlterField(
            model_name="sermonbiblepassage",
            name="type",
            field=models.IntegerField(
                choices=[
                    (3, "EPISTLE (or Acts / Revelation)"),
                    (1, "PROPHECY (or other Old Testament)"),
                    (4, "GOSPEL"),
                    (5, "OTHER"),
                    (2, "PSALM"),
                ],
                default=0,
            ),
        ),
        migrations.CreateModel(
            name="SermonLocation",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("website", models.URLField(blank=True, null=True)),
                (
                    "alternate_names",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        blank=True,
                        help_text="A list of strings to be matched when importing a sermon.",
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "address",
                    address.models.AddressField(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="address.Address"
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]