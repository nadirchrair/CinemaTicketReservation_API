from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Movies)
admin.site.register(Guest)
admin.site.register(Reservation)