# Generated by Django 4.0 on 2021-12-21 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('published_at', models.DateTimeField()),
                ('thumbnail_URL', models.URLField(max_length=500)),
            ],
            options={
                'ordering': ('-published_at',),
            },
        ),
    ]
