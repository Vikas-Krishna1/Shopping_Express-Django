from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile (models.Model):
    USER_TYPE = (
        ('CUSTOMER', 'Customer'),
        ('EMPLOYEE', 'Employee'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='CUSTOMER')
    
   
    

    def __str__(self):
        return self.user.username
    
class Address(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
       return f"{self.user.username} Address"
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
