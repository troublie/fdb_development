# Generated by Django 2.0.2 on 2018-02-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuji', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
