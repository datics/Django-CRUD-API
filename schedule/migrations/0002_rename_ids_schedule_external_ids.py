# Generated by Django 5.2.3 on 2025-06-13 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='ids',
            new_name='external_ids',
        ),
    ]
