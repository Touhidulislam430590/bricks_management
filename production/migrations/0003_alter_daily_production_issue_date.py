# Generated by Django 5.0.2 on 2024-04-20 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_daily_production_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_production',
            name='issue_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
