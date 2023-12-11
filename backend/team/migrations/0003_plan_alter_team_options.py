# Generated by Django 4.2 on 2023-12-11 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_rename_memeber_team_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('max_leads', models.IntegerField()),
                ('max_clients', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ('name',)},
        ),
    ]