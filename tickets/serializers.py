from rest_framework import serializers
from tickets.models import *
class MoviesSerialzer(serializers.ModelSerializer):
    class Meta:
        model= Movies
        fields ='__all__'
    
        
class ReservationSerialzer(serializers.ModelSerializer):
    class Meta:
        model= Reservation
        fields ='__all__'     

class GuestSerialzer(serializers.ModelSerializer):
    class Meta:
        model= Guest
        fields =['pk','reservation','name','mobile']                 