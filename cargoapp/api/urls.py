from django.urls import path
from . import views
from django.contrib.auth  import views as auth_views

urlpatterns = [
    path('register/',views.UserRegister.as_view(), name='register'),
    
    path('login/', views.UserLogin.as_view(), name='login'),
    
	path('logout/', views.UserLogout.as_view(), name='logout'),
 
	path('user/', views.UserView.as_view(), name='user'),
 
    path('alltrips/',views.AllTrips.as_view(), name="all_trips"),

    path('mytrips/',views.MyTrips.as_view(), name="my_trips"),

    path('create/',views.CreateTrip.as_view(), name="all_trips"),

    path('book/',views.BookTrip.as_view(), name="all_trips"),

]