from django.db import models

# Create your models here.
class crimeSen(models.Model):
    index=models.AutoField(primary_key=True)
    title=models.TextField()
    location=models.TextField(null=True)
    date=models.TextField(null=True)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)

class calamitySen(models.Model):
    index=models.AutoField(primary_key=True)
    title=models.TextField()
    dead=models.IntegerField(default=100)
    injured=models.IntegerField(default=100)
    peopleAffected=models.IntegerField(default=100)
    cost=models.IntegerField(default=100)
    police=models.IntegerField(default=100)
    ambulance=models.IntegerField(default=100)
    ndrfPersonnels=models.IntegerField(default=100)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)

class epidemicSen(models.Model):
    class Type(models.IntegerChoices):
        Deadly=1
        Infectious=2
        Seasonal=3

    index=models.AutoField(primary_key=True)
    title=models.TextField()
    infected=models.IntegerField(default=100)
    cured=models.IntegerField(default=100)
    died=models.IntegerField(default=100)
    year=models.TextField(null=True)
    hospitalBed=models.IntegerField(default=100)
    healthStaff=models.IntegerField(default=100)
    type=models.IntegerField(choices=Type.choices, default=Type.Seasonal)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)



class publicGatheringSen(models.Model):
    class Type(models.IntegerChoices):
        Political=1
        Social=2
        Protest=3
        Government=4
        Religious=5
    
    index=models.AutoField(primary_key=True)
    title=models.TextField()
    type=models.IntegerField(choices=Type.choices, default=Type.Protest)
    attendance=models.IntegerField(default=100)
    police=models.IntegerField(default=100)
    ambulance=models.IntegerField(default=100)
    fireFighter=models.IntegerField(default=100)
    location=models.TextField(null=False)
    date=models.TextField(null=True)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)

class rallySen(models.Model):
    class Type(models.IntegerChoices):
        Political=1
        Social=2
        Protest=3
        Government=4
        Religious=5

    index=models.AutoField(primary_key=True)
    title=models.TextField()
    attendance=models.IntegerField(default=100)
    police=models.IntegerField(default=100)
    ambulance=models.IntegerField(default=100)
    fireFighter=models.IntegerField(default=100)
    location=models.TextField(null=False)
    type=models.IntegerField(choices=Type.choices, default=Type.Protest)
    lesson=models.TextField(null=False)
    count=models.IntegerField(default=1)