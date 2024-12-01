from django.db import models
from django.contrib.auth.models import User


class department(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self): return self.name 


class employee(models.Model):

    name=models.CharField(max_length=50)
    designation=models.ForeignKey(department,on_delete=models.CASCADE)
    salary=models.IntegerField()
    experience=models.IntegerField(default=2)


    def __str__(self): return self.name 

    

