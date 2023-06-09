from django.db import models
from django.contrib.postgres.fields import JSONField

class Rally(models.Model):

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rally_title = models.TextField( blank=False)
    religious = models.BooleanField(default=False)
    political = models.BooleanField(default=False)
    social = models.BooleanField(default=False)
    protest = models.BooleanField(default=False)
    government = models.BooleanField(default=False)
    attendance = models.IntegerField(blank=False)
    stationary = models.BooleanField(default = False)
    start_location = models.CharField( max_length=50, blank = False,default="Random")
    end_location = models.CharField(max_length=50, blank = True, null=True ,default="Random")
    police = models.IntegerField(blank=False, default=0)
    ambulance = models.IntegerField(blank=False, default=0)
    firefighters = models.IntegerField(blank=False, default=0)
    date = models.DateField(blank=True, null=True)
    lesson_learnt = models.TextField(blank = False)

def __str__(self):
        return self.rally_title