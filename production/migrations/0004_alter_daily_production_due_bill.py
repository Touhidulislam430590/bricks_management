# Generated by Django 5.0.2 on 2024-04-29 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_alter_daily_production_issue_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily_production',
            name='due_bill',
            field=models.IntegerField(default=0),
        ),
    ]
