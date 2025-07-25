# Generated by Django 5.1.4 on 2025-01-20 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_user_inviter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestplayer',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='guestplayer',
            name='cup',
        ),
        migrations.RemoveField(
            model_name='guestplayer',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='guestplayer',
            name='is_blocked',
        ),
        migrations.RemoveField(
            model_name='guestplayer',
            name='score',
        ),
        migrations.RemoveField(
            model_name='guestplayer',
            name='xp',
        ),
        migrations.RemoveField(
            model_name='normalplayer',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='normalplayer',
            name='cup',
        ),
        migrations.RemoveField(
            model_name='normalplayer',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='normalplayer',
            name='is_blocked',
        ),
        migrations.RemoveField(
            model_name='normalplayer',
            name='score',
        ),
        migrations.RemoveField(
            model_name='normalplayer',
            name='xp',
        ),
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='Birth date'),
        ),
        migrations.AddField(
            model_name='user',
            name='cup',
            field=models.PositiveIntegerField(default=0, verbose_name='Cup'),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(choices=[(1, 'MALE'), (2, 'FEMALE'), (0, 'UNKNOWN')], default=0, verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='Is blocked'),
        ),
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.PositiveIntegerField(default=0, verbose_name='Score'),
        ),
        migrations.AddField(
            model_name='user',
            name='xp',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Xp'),
        ),
    ]
