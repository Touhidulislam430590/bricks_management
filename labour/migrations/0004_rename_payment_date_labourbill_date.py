# Generated by Django 5.0.2 on 2024-04-30 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0003_alter_labourdeal_payment_sequence'),
    ]

    operations = [
        migrations.RenameField(
            model_name='labourbill',
            old_name='payment_date',
            new_name='date',
        ),
    ]
