from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import  Token
from django.conf import settings
# Create your models here.

class Movies(models.Model):
    hall = models.CharField(max_length=20)
    movie= models.CharField(max_length=20)
    date= models.DateField()
    def __str__(self):
        return self.movie
    



   
class Guest(models.Model):
    name=models.CharField(max_length=50)
    mobile= models.CharField(max_length=10)
    def __str__(self):
        return self.name
class Reservation(models.Model):
    guest=models.ForeignKey(Guest,related_name="reservation",on_delete=models.CASCADE)
    movies=models.ForeignKey(Movies,related_name="movies",on_delete=models.CASCADE)
    
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender,created,instance, **kwargs):
    if created:
                Token.objects.create(user=instance)
    

  
