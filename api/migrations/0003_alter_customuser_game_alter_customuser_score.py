# Generated by Django 4.2.1 on 2023-05-13 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_customuser_score_game_code_alter_game_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='api.game'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
