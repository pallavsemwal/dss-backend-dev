from django.db import models
class searchResult(models.Model):
    query= models.CharField(max_length=1000)
    websiteLink=models.CharField(max_length=1000)
    department= models.IntegerField() 
    list1= models.IntegerField()
    list2= models.IntegerField()
    description= models.IntegerField()
    


