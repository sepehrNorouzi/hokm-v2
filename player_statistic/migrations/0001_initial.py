# Generated by Django 5.1.4 on 2025-01-24 10:57

import django.db.models.deletion
import player_statistic.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0007_alter_rewardpackage_reward_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('start_xp', models.PositiveIntegerField(default=0, verbose_name='Start Xp')),
                ('reward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.rewardpackage', verbose_name='Level Up reward')),
            ],
            options={
                'verbose_name': 'Player Level',
                'verbose_name_plural': 'Player Levels',
                'ordering': ['start_xp'],
            },
        ),
        migrations.CreateModel(
            name='PlayerStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('prev_xp', models.PositiveIntegerField(default=0, editable=False, verbose_name='Prev Xp')),
                ('score', models.PositiveIntegerField(default=0, verbose_name='Score')),
                ('xp', models.PositiveIntegerField(default=0, editable=False, verbose_name='Xp')),
                ('cup', models.PositiveIntegerField(default=0, verbose_name='Cup')),
                ('level', models.ForeignKey(default=player_statistic.models.PlayerLevel.get_first_level, editable=False, on_delete=django.db.models.deletion.SET_DEFAULT, to='player_statistic.playerlevel', verbose_name='Level')),
                ('player', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to=settings.AUTH_USER_MODEL, verbose_name='Player')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
