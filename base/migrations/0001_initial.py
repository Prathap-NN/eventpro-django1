# Generated by Django 4.1 on 2022-09-07 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=191, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('event_start_date', models.DateField(blank=True, null=True)),
                ('event_end_date', models.DateField(blank=True, null=True)),
                ('department', models.CharField(blank=True, max_length=191, null=True)),
                ('campus', models.CharField(blank=True, max_length=191, null=True)),
                ('tags', models.CharField(blank=True, max_length=191, null=True)),
                ('email', models.CharField(blank=True, max_length=191, null=True)),
                ('event_start_time', models.CharField(blank=True, max_length=10, null=True)),
                ('event_end_time', models.CharField(blank=True, max_length=10, null=True)),
                ('contact', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('is_online_event', models.CharField(blank=True, max_length=3, null=True)),
                ('website', models.CharField(blank=True, max_length=191, null=True)),
                ('facebook', models.CharField(blank=True, max_length=191, null=True)),
                ('youtube', models.CharField(blank=True, max_length=191, null=True)),
                ('instagram', models.CharField(blank=True, max_length=191, null=True)),
                ('twitter', models.CharField(blank=True, max_length=191, null=True)),
                ('featured_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('attachment', models.TextField(blank=True, null=True)),
                ('view_count', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('external_link', models.TextField(blank=True, null=True)),
                ('club_name', models.CharField(blank=True, max_length=191, null=True)),
                ('button_name', models.CharField(blank=True, max_length=20, null=True)),
                ('custom_text', models.CharField(blank=True, max_length=100, null=True)),
                ('event_attendees', models.CharField(blank=True, max_length=10, null=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('publish', models.CharField(blank=True, max_length=20, null=True)),
                ('google_map', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Speakers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=191)),
                ('profile_pic', models.ImageField(max_length=191, upload_to='speakers/')),
                ('about', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.events')),
            ],
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_images', models.ImageField(upload_to='Uploads')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.events')),
            ],
        ),
        migrations.CreateModel(
            name='Brochures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='brochures/')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.events')),
            ],
        ),
    ]
