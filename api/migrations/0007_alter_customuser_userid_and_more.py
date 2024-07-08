# Generated by Django 5.0.6 on 2024-07-06 18:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_customuser_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='userId',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.TextField(),
        ),
    ]
