# Generated by Django 5.0.2 on 2024-04-20 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='daily_production',
            name='issue_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
