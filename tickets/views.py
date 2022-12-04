from django.shortcuts import render
from django.http.response import JsonResponse 
from .models import Guest , Movies, Reservation
from rest_framework.decorators import api_view
from rest_framework import status , filters
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics , mixins , viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication , TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *
# Create your views here.
####"1" whitout Rest and not query  model fbv
def no_rest_no_model(request):
    guest=[
        {
            'id':1,
            'name':'omar',
            'mobile':1225740
            
        },
        {
            'id':2,
            'name':'nadir',
            'mobile':1225740
            
        },
        {
            'id':3,
            'name':'zaki',
            'mobile':1225740
            
        },
         ] 
    return JsonResponse(guest, safe=False)
    
 #2  model data default django  without rest
def no_rest_from_model(request):    
    data=Guest.objects.all()
    response={
        'geust':list(data.values('name','mobile'))
    }
    return JsonResponse(response)
#3-create:post 
# - list : get
#pk_query :GET
# Updat : put
# delete :destory

# 4 function Based Views
#4.1 GET POST
@api_view(['GET','POST'])
def FBV_list(request):
    #GET
    if request.method== 'GET':
        guests= Guest.objects.all()
        serializer= GuestSerialzer(guests, many=True)
        
        return Response(serializer.data)
    
    
    
    #POST
    elif request.method == 'POST' :
        serializer = GuestSerialzer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)



#4.2 GET PUT DELETE POST
@api_view(['GET','PUT', 'DELETE'])
def FBV_pk(request, pk):
    guests= Guest.objects.get(pk=pk)

    if request.method== 'GET':
        serializer= GuestSerialzer(guests)
        return Response(serializer.data)
    
    
    #PUUT
    elif request.method == 'PUT' :
        serializer = GuestSerialzer(guests,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    #DELETE
    elif request.method == 'DELETE' :
        guests.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
### clased Based views
class CBV_LIST(APIView):
    def get(self, request):
        geust = Guest.objects.all()
        serialzer = GuestSerialzer(geust, many=True)
        return Response(serialzer.data)
    def post(self, request):
        serialzer = GuestSerialzer(data=request.data )
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status = status.HTTP_201_CREATED)
        return Response(serialzer.data, status = status.HTTP_400_BAD_REQUEST)    
       
#5#5# MIxines 
#     post get
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset=Guest.objects.all()
    searailzer_class=GuestSerialzer
    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)
    
           
#5#5# MIxines 
#    put get delete
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    searailzer_class=GuestSerialzer
    def get(self,request,pk):
        return self.retrieve(request)
    
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)
###66# generics 
#6.1 get and post

class generics_views(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerialzer
    authentication_classes = [TokenAuthentication]
   # permission_classes = [IsAuthenticated]
#6.2 get put and delete

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerialzer
    authentication_classes = [TokenAuthentication]
   # permission_classes = [IsAuthenticated]
### 7 viewsets
class viewset_guest(viewsets.ModelViewSet):
     queryset=Guest.objects.all()
     serializer_class =GuestSerialzer
    # movie
class viewset_movie(viewsets.ModelViewSet):
     queryset=  Movies.objects.all()
     serializer_class =MoviesSerialzer
     filter_backend=[filters.SearchFilter]
     search_fileds=['movie']
     
class viewset_reservation(viewsets.ModelViewSet):
     queryset=Reservation.objects.all()
     serializer_class =ReservationSerialzer

@api_view(['GET'])
def find_movie(request):
    movies= Movies.objects.filter(
        movie=request.data['movie']
        
    )     
    serializer = MoviesSerialzer(movies, many=True)
    return Response(serializer.data)
     
     

@api_view(['POST'])
def new_reservation(request):
    movie = Movies.objects.get(       
            hall=request.data['hall'],
            movie=request.data['movie'],  
    )     
    guest= Guest()
    guest.name=request.data['name'],
    guest.mobile=request.data['mobile'],
    guest.save()
    reservation = Reservation()
    reservation.guest=guest
    reservation.movies= movie
    reservation.save()
    serializer= ReservationSerialzer(reservation)
      
    return Response(serializer.data,status = status.HTTP_201_CREATED)
