# Generated by Django 3.2.3 on 2021-09-13 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.TextField(max_length=100)),
                ('club_photo', models.ImageField(upload_to='clubs_photo')),
                ('club_slug', models.SlugField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.TextField(default='', max_length=255)),
                ('post_text', models.TextField(default='', max_length=3000)),
                ('post_image', models.ImageField(upload_to='posts_photo')),
                ('post_published', models.CharField(default='', max_length=50)),
                ('post_creator', models.CharField(default='', max_length=255)),
                ('post_slug', models.SlugField(default='', unique=True)),
                ('post_date', models.DateField()),
                ('post_club', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='main.club')),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
    ]
