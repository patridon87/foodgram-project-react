# Generated by Django 2.2.19 on 2022-01-27 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"ordering": ["-id"]},
        ),
    ]