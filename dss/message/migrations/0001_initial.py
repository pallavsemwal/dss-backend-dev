# Generated by Django 3.0.4 on 2023-02-12 04:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('messageId', models.CharField(editable=False, max_length=1000, primary_key=True, serialize=False)),
                ('senderId', models.IntegerField()),
                ('receiverId', models.IntegerField()),
                ('messageType', models.CharField(choices=[('notice', 'Notice'), ('doable', 'Doable')], default='notice', max_length=20)),
                ('messageContent', models.CharField(max_length=1000)),
                ('relatedDocumentLink', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1000), null=True, size=None)),
                ('timestampCreation', models.DateTimeField(max_length=10)),
                ('doableId', models.UUIDField(null=True)),
            ],
        ),
    ]
