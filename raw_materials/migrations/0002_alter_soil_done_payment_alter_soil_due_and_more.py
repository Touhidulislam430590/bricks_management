# Generated by Django 5.0.2 on 2024-04-16 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raw_materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soil',
            name='done_payment',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='soil',
            name='due',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='soil',
            name='quantity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='soil',
            name='rate',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='soil',
            name='total_price',
            field=models.FloatField(),
        ),
    ]
