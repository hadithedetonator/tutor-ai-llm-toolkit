from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.
class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
