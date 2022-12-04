from django.contrib import admin
from django.urls import path , include
from tickets import views
from tickets.views import viewset_guest, viewset_movie , viewset_reservation
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('viewset', viewset_guest, basename='viewset')
router.register('movie', viewset_movie, basename='movie')
router.register('reservation', viewset_reservation, basename='reservation')

urlpatterns = router.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/jsonresponsenomodel/', views.no_rest_no_model),
    #2
        path('django/jsonresponsefrommodel/', views.no_rest_from_model),
#3
        path('django/rest_freamwork/', views.FBV_list),

#4
        path('django/rest_freamwork/<int:pk>', views.FBV_pk),
        
#5
        path('django/CBV/', views.CBV_LIST.as_view()),
        ## generics
                path('django/generics/', views.generics_views.as_view()),
        path('django/generics/<int:pk>', views.generics_pk.as_view()),

              
#7
        path('rest/viewsets/', include(router.urls)),      
#8
        path('django/movie/', views.find_movie),
        #8
        path('django/new_reservation/', views.new_reservation),
        #rest framwork auth
        path('api-auth',include('rest_framework.urls')),
# 11 Token authentication
path('api-token-auth',obtain_auth_token)

]
