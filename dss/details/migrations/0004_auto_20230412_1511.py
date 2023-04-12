# Generated by Django 3.2 on 2023-04-12 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0003_rename_lessons_learnt_publicgathering_lesson_learnt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rally',
            old_name='lessons_learnt',
            new_name='lesson_learnt',
        ),
        migrations.AlterField(
            model_name='rally',
            name='end_location',
            field=models.CharField(blank=True, default='Random', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rally',
            name='start_location',
            field=models.CharField(default='Random', max_length=50),
        ),
    ]