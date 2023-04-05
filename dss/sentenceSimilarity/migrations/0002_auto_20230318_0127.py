# Generated by Django 3.0.4 on 2023-03-18 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sentenceSimilarity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicgatheringsen',
            name='date',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='publicgatheringsen',
            name='type',
            field=models.IntegerField(choices=[(1, 'Political'), (2, 'Social'), (3, 'Protest'), (4, 'Government'), (5, 'Religious')], default=3),
        ),
    ]
