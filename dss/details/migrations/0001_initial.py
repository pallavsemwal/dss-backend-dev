# Generated by Django 3.2 on 2023-04-12 12:05

from django.conf import settings
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('departmentId', models.AutoField(primary_key=True, serialize=False)),
                ('departmentName', models.CharField(editable=False, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('area', models.IntegerField(blank=True)),
                ('state', models.CharField(max_length=20)),
                ('location', models.CharField(blank=True, max_length=25)),
                ('population', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=70)),
                ('is_all_day', models.BooleanField(default=False)),
                ('start_date_time', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=30)),
                ('end_date_time', models.DateTimeField()),
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Normal'), (3, 'High')], default=2)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('mom', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
                ('recipients', models.ManyToManyField(blank=True, related_name='shared_with_me_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['start_date_time'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50)),
                ('task_date', models.DateField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['task_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('details', models.TextField(blank=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='own_tags', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('details', models.TextField(blank=True)),
                ('num_people_reached', models.IntegerField(default=0)),
                ('num_people_left', models.IntegerField(default=0)),
                ('image', models.ImageField(default='schemes/default.jpg', upload_to='schemes/')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='schemes', to='details.district')),
            ],
            options={
                'ordering': ['-num_people_reached'],
            },
        ),
        migrations.CreateModel(
            name='Rally',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rally_title', models.TextField()),
                ('religious', models.BooleanField(default=False)),
                ('political', models.BooleanField(default=False)),
                ('social', models.BooleanField(default=False)),
                ('protest', models.BooleanField(default=False)),
                ('government', models.BooleanField(default=False)),
                ('attendance', models.IntegerField()),
                ('stationary', models.BooleanField(default=False)),
                ('start_location', models.CharField(max_length=50)),
                ('end_location', models.CharField(blank=True, max_length=50, null=True)),
                ('police', models.IntegerField(default=0)),
                ('ambulance', models.IntegerField(default=0)),
                ('firefighters', models.IntegerField(default=0)),
                ('date', models.DateField(blank=True, null=True)),
                ('lessons_learnt', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PublicGathering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('religious', models.BooleanField(default=False)),
                ('political', models.BooleanField(default=False)),
                ('social', models.BooleanField(default=False)),
                ('protest', models.BooleanField(default=False)),
                ('government', models.BooleanField(default=False)),
                ('attendance', models.IntegerField()),
                ('close', models.BooleanField(default=False)),
                ('location', models.CharField(max_length=50)),
                ('police', models.IntegerField(default=0)),
                ('ambulance', models.IntegerField(default=0)),
                ('firefighters', models.IntegerField(default=0)),
                ('date', models.DateField(blank=True, null=True)),
                ('duration', models.IntegerField()),
                ('lessons_learnt', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='auth.user')),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', max_length=7)),
                ('dob', models.DateField(blank=True)),
                ('rank', models.CharField(blank=True, max_length=25)),
                ('batch', models.PositiveSmallIntegerField(blank=True)),
                ('image', models.ImageField(default='profile_pics/default.png', upload_to='profile_pics/')),
                ('mobileNumber', models.CharField(blank=True, max_length=12)),
                ('departments', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('district', models.ManyToManyField(to='details.District')),
            ],
        ),
        migrations.CreateModel(
            name='LawAndOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('situation_type', models.CharField(choices=[('rally', 'Rally'), ('gathering', 'Gathering'), ('epidemic', 'Epidemic'), ('calamity', 'Calamity'), ('crime', 'Crime')], default='rally', max_length=15)),
                ('configuration', django.contrib.postgres.fields.jsonb.JSONField()),
                ('arrangements', django.contrib.postgres.fields.jsonb.JSONField()),
                ('related_event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='law_and_order', to='details.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='materials/')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files', to='details.event')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='events_of_tag', to='details.Tag'),
        ),
        migrations.CreateModel(
            name='Epidemic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('epidemic_type', models.CharField(default='trivial', max_length=50)),
                ('total_infected', models.IntegerField(default=0)),
                ('cured', models.IntegerField(default=0)),
                ('died', models.IntegerField(default=0)),
                ('year', models.IntegerField(default=2020)),
                ('date', models.DateField(blank=True, null=True)),
                ('police', models.IntegerField(default=0)),
                ('hospitalbeds', models.IntegerField(default=0)),
                ('healthstaff', models.IntegerField(default=0)),
                ('lesson_learnt', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Crime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('crime_type', models.CharField(choices=[('Murder', 'Murder'), ('Rape', 'Rape'), ('Kidnapping', 'Kidnapping'), ('Loot', 'Loot'), ('Robbery', 'Robbery'), ('Smuggling', 'Smuggling'), ('Other', 'Other')], default='Other', max_length=20)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('lesson_learnt', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_time'],
            },
        ),
        migrations.CreateModel(
            name='Calamity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('calamity_type', models.CharField(choices=[('Floods', 'Floods'), ('Drought', 'Drought'), ('Earthquake', 'Earthquake'), ('Forest Fire', 'Forestfire'), ('Cyclone', 'Cyclone'), ('Landslide', 'Landslide'), ('Storm', 'Storm'), ('Other', 'Other')], default='Other', max_length=20)),
                ('total_cost', models.BigIntegerField(default=0)),
                ('injured', models.IntegerField(default=0)),
                ('dead', models.IntegerField(default=0)),
                ('people_affected', models.IntegerField(default=0)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
                ('police', models.IntegerField(default=0)),
                ('ambulance', models.IntegerField(default=0)),
                ('ndrf', models.IntegerField(default=0)),
                ('lesson_learnt', models.TextField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
