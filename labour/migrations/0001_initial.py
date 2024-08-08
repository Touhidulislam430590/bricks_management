# Generated by Django 5.0.2 on 2024-03-18 18:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LabourDeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sarder_name', models.CharField(max_length=100)),
                ('payment_sequence', models.CharField(choices=[('Monthly', 'Monthly'), ('Weekly', 'Weekly'), ('Daily', 'Daily')], max_length=20)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('requirements', models.TextField()),
                ('issue_date', models.DateTimeField(auto_now=True)),
                ('number_of_employee', models.IntegerField()),
                ('starting_date', models.DateField()),
                ('closing_date', models.DateField()),
                ('season_target', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LabourType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LabourBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('labour_section', models.CharField(blank=True, max_length=100)),
                ('sarder_name', models.CharField(blank=True, max_length=100)),
                ('bill_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('labour_deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labour.labourdeal')),
            ],
        ),
        migrations.AddField(
            model_name='labourdeal',
            name='labour_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labour.labourtype'),
        ),
    ]