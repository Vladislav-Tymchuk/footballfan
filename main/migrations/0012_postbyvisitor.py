# Generated by Django 3.2.3 on 2021-09-25 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_delete_postbyvisitor'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostByVisitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.TextField(max_length=255)),
                ('post_text', models.TextField(max_length=4095)),
                ('post_image', models.ImageField(upload_to='posts_photo')),
                ('post_date', models.DateTimeField()),
                ('post_club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.club')),
                ('post_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
