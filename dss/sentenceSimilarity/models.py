from django.db import models
from details.models.calamity import Calamity
from details.models.crime import Crime
from details.models.epidemic import Epidemic
from details.models.publicGathering import PublicGathering
from details.models.rally import Rally

# Create your models here.
class crimeSen(models.Model):
    index=models.AutoField(primary_key=True)
    detailId=models.ForeignKey(Crime,on_delete=models.CASCADE)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)

class calamitySen(models.Model):
    index=models.AutoField(primary_key=True)
    detailId=models.ForeignKey(Calamity,on_delete=models.CASCADE)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)

class epidemicSen(models.Model):
    index=models.AutoField(primary_key=True)
    detailId=models.ForeignKey(Epidemic,on_delete=models.CASCADE)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)


class publicGatheringSen(models.Model):
    index=models.AutoField(primary_key=True)
    detailId=models.ForeignKey(PublicGathering,on_delete=models.CASCADE)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)

class rallySen(models.Model):
    index=models.AutoField(primary_key=True)
    detailId=models.ForeignKey(Rally,on_delete=models.CASCADE)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)