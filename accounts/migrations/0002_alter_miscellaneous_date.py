# Generated by Django 5.0.2 on 2024-03-20 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miscellaneous',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
