# Generated by Django 2.1.7 on 2019-02-26 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0020_auto_20190225_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='lecture_id',
            new_name='lecture',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='student_id',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='attendance',
            old_name='subject_id',
            new_name='subject',
        ),
    ]
