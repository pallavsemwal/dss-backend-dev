# Generated by Django 3.2 on 2023-04-12 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('details', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rallySen',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.TextField()),
                ('count', models.IntegerField(default=1)),
                ('detailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.rally')),
            ],
        ),
        migrations.CreateModel(
            name='publicGatheringSen',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.TextField()),
                ('count', models.IntegerField(default=1)),
                ('detailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.publicgathering')),
            ],
        ),
        migrations.CreateModel(
            name='epidemicSen',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.TextField()),
                ('count', models.IntegerField(default=1)),
                ('detailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.epidemic')),
            ],
        ),
        migrations.CreateModel(
            name='crimeSen',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.TextField()),
                ('count', models.IntegerField(default=1)),
                ('detailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.crime')),
            ],
        ),
        migrations.CreateModel(
            name='calamitySen',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('lesson', models.TextField()),
                ('count', models.IntegerField(default=1)),
                ('detailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='details.calamity')),
            ],
        ),
    ]
