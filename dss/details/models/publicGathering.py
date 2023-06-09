from django.db import models
from django.contrib.postgres.fields import JSONField

class PublicGathering(models.Model):

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.TextField( blank=False)
    religious = models.BooleanField(default=False)
    political = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    protest = models.BooleanField(default=False)
    government = models.BooleanField(default=False)
    attendance = models.IntegerField(blank=False)
    close = models.BooleanField(default = False)
    location = models.TextField(blank = False)
    police = models.IntegerField(blank=False, default=0)
    ambulance = models.IntegerField(blank=False, default=0)
    firefighters = models.IntegerField(blank=False, default=0)
    date = models.DateField(blank=True, null=True)
    duration = models.IntegerField(blank=False)
    lesson_learnt = models.TextField(blank=False)

def __str__(self):
        return self.title