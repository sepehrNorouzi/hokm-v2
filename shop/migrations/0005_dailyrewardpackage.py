# Generated by Django 5.1.4 on 2025-01-16 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_rewardpackage_support_type_rewardpackage_vip_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyRewardPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('day_number', models.PositiveIntegerField(default=1, unique=True, verbose_name='Day number')),
                ('reward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.rewardpackage', verbose_name='Reward')),
            ],
            options={
                'verbose_name': 'Daily Reward',
                'verbose_name_plural': 'Daily Rewards',
                'ordering': ('day_number',),
            },
        ),
    ]
