# Generated by Django 2.2.19 on 2022-01-27 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220127_1451'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['-id']},
        ),
    ]
