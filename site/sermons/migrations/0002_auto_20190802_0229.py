# Generated by Django 2.2.3 on 2019-08-02 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("sermons", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="sermon",
            name="text",
            field=models.TextField(
                blank=True, help_text="The full content of the sermon", null=True, verbose_name="Text"
            ),
        )
    ]