# Generated by Django 5.1.4 on 2025-01-19 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friendshiprequest',
            options={'ordering': ['created_time'], 'verbose_name': 'Friendship Request', 'verbose_name_plural': 'Friendship Requests'},
        ),
    ]
