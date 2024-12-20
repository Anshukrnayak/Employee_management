from django.db import models
from django.contrib.auth.models import User

class AgentModel(models.Model):

    designation_choice=(
        ('Engineer','Engineer'),
        ('CA','Charted Accountant'),
        ('PM','product manager'),
        ('Sales manager','sales manager')
    )
    profile_image=models.ImageField(upload_to='profile_image')
    name=models.ForeignKey(User,on_delete=models.CASCADE,related_name='agent')
    desigation=models.CharField(choices=designation_choice,max_length=50)
    experience=models.IntegerField(default=2)

    def __str__(self): return  self.name.username

class LeadModel(models.Model):

    agent=models.ForeignKey(User,on_delete=models.CASCADE,related_name='lead')
    profile_image=models.ImageField(upload_to='profile_image')
    name=models.CharField(max_length=50)
    email=models.EmailField()
    contact=models.IntegerField()
    

    def __str__(self): return self.name 

