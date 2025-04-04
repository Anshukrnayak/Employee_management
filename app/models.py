from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Fixed field name

    class Meta:
        abstract = True


class LeadModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lead')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    location = models.TextField()
    about = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics')  # Renamed for better file organization

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class ClientModel(BaseModel):
    lead = models.ForeignKey(LeadModel, on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    email = models.EmailField(unique=True)  # Ensuring unique email for each client
    location = models.TextField()
    about = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Done', 'Done'),
            ('Process', 'Process')  # Capitalized for consistency
        ],
        default=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
