# Generated by Django 4.2.7 on 2025-05-05 04:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('materials', '0002_alter_course_preview_alter_lesson_preview'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owned_courses', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owned_lessons', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
            preserve_default=False,
        ),
    ]
