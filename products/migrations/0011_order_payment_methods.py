# Generated by Django 4.2.10 on 2024-06-10 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_methods',
            field=models.CharField(choices=[('1', 'Zelle'), ('2', 'Venmo'), ('3', 'Apple Pay'), ('4', 'WeChat'), ('5', 'Direct Bank Transfer'), ('6', 'Western Union Transfer')], default='1', max_length=1),
        ),
    ]