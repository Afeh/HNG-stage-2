# Generated by Django 5.0.6 on 2024-07-05 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_organisation_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='orgId',
        ),
    ]
