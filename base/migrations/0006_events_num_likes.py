# Generated by Django 4.0 on 2022-09-11 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_events_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='num_likes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
