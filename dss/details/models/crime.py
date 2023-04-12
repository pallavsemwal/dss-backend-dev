from django.db import models
from django.contrib.postgres.fields import JSONField


class Crime(models.Model):
    class CrimeTypes(models.TextChoices):
        MURDER = "Murder"
        RAPE =  "Rape"
        KIDNAPPING = "Kidnapping"
        LOOT = "Loot"
        ROBBERY = "Robbery"
        SMUGGLING = "Smuggling"
        OTHER = "Other"
        
       

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(blank=False, null=True)
    crime_type = models.CharField(max_length=20, choices=CrimeTypes.choices, default=CrimeTypes.OTHER)
    area = models.CharField(blank=True,null=True)
    date_time = models.DateTimeField(blank=True,null=True)
    lesson_learnt = models.TextField(blank=True,null=True)


    class Meta:
        ordering = ['date_time']


def __str__(self):
        return self.title