# Generated by Django 4.2.10 on 2024-02-21 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_stateofproduct_title2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stateofproduct',
            name='title2',
        ),
    ]