# Generated by Django 3.2 on 2023-04-12 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='searchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=1000)),
                ('websiteLink', models.CharField(max_length=1000)),
                ('department', models.IntegerField()),
                ('list1', models.IntegerField()),
                ('list2', models.IntegerField()),
                ('description', models.IntegerField()),
            ],
        ),
    ]
