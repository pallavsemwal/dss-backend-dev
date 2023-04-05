from django.db import models

# Create your models here.
class scheme1(models.Model):

    date=models.DateField(null=False)
    csc_covered=models.IntegerField(null=False)
    enrollments=models.IntegerField(null=False)
