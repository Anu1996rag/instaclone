# Generated by Django 4.1.7 on 2023-04-12 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
