# Generated by Django 5.0.2 on 2024-02-23 22:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateTimeField(db_index=True)),
                ('categories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, size=None)),
                ('content', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
