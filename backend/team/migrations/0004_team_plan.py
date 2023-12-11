# Generated by Django 4.2 on 2023-12-11 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_plan_alter_team_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='plan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teamsplan', to='team.plan'),
            preserve_default=False,
        ),
    ]