# Generated by Django 5.0.2 on 2024-02-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.TextField(max_length=20)),
                ('cmobile', models.TextField(max_length=14)),
                ('caddress', models.TextField(max_length=100)),
            ],
        ),
    ]
