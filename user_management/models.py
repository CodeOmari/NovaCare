from django.db import models
from django.contrib.auth.models import User

import os
import uuid

def generate_unique_name(instance, filename):
    name = uuid.uuid4()
    full_filename = f'{name}-{filename}'
    return os.path.join("profile_pictures", full_filename)

# Create your models here.
class Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='-')
    last_name = models.CharField(max_length=50, default='-')
    phone_number = models.CharField(max_length=15, default='-')
    dob = models.DateField(default='2025-01-01')
    identity_type = models.CharField(max_length=30, default='-')
    identity_number = models.CharField(max_length=30, default='-')
    gender = models.CharField(max_length=6, default='-')
    profile_pic = models.ImageField(upload_to=generate_unique_name, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'
    
    class Meta:
        db_table = 'Personal_Details'