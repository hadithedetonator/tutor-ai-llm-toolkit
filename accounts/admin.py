from django.contrib import admin
from .models import CustomUser
# Register your models here.

# Register the custom User model
admin.site.register(CustomUser)
