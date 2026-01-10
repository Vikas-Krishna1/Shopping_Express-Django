from django.db import models
from django.conf import settings
from items.models import Item
from accounts.models import User,Profile

User = settings.AUTH_USER_MODEL

# Create your models here.
class CartItem(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     item = models.ForeignKey(Item, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField()

class Meta:
    unique_together = ('user', 'item')

def __str__(self):
        return f"{self.user} - {self.item}"


	
	

