# Generated by Django 5.0.2 on 2024-04-08 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selling', '0003_alter_selling_due_alter_selling_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='selling',
            name='issue_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
