from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from app import choices


# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True) #using OneToOneField to create a one to one relationship with the User model registered in settings. This will create a user for each employee. if we use ForeignKey, it will create a many to one relationship with the user model.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True) #upload_to specifies the directory where the image will be uploaded. blank=True allows the field to be empty in the form, null=True allows the field to be empty in the database.

    def __str__(self):
        return f"{self.first_name} {self.department}"

class Inventory(models.Model):
    product_name = models.CharField(max_length=100)
    product_id = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_id} {self.product_name}"
    
class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) #using models.CASCADE to delete the leave record if the employee is deleted. if we use models.SET_NULL, the leave record will be set to null if the employee is deleted. if we use models.PROTECT, it will raise an error if we try to delete the employee who has leave records.
    leave_type = models.CharField(max_length=50, choices=choices.leave_type)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=choices.leave_status, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"

class User(AbstractUser):
    # Add any additional fields you want to include in your custom user model
    # For example: phone_number = models.CharField(max_length=15)
    
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' #makes email the login field instead of username
    # The field that will be used to create the user. This is the field that will be used to authenticate the user.

    REQUIRED_FIELDS = ['username'] # The fields that are required when creating a user. These fields will be prompted when creating a user.
