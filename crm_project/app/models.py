from django.db import models
from django.contrib.auth.models import User

class PersonalDetailModel(models.Model):

    image=models.ImageField(upload_to='profile/')
    name=models.CharField(max_length=50)
    location=models.CharField(max_length=250)
    contact=models.IntegerField()
    email=models.EmailField()
    joining_date=models.DateField(auto_now_add=True)


    def __str__(self): return self.name 


class DesignationModel(models.Model):
    designation=models.CharField(max_length=50)

    def __str__(self): return self.designation


class LeadModel(PersonalDetailModel):

    lead=models.ForeignKey(User,on_delete=models.CASCADE,related_name='lead')
    designation=models.ForeignKey(DesignationModel,on_delete=models.CASCADE)
    experience=models.PositiveIntegerField()
    salary=models.PositiveIntegerField()

    def __str__(self): return f'{self.lead.lead}'


class ClientModel(PersonalDetailModel):
    status=models.CharField(max_length=50,choices=(('process','process'),('Pending','Pending'),('success','success')))
    manage_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='client')
    description=models.TextField()

    


    
