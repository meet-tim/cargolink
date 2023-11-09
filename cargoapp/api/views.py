from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer,TripSerializer,BookingSerializer,DriverSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import Trip,AppUser,Booking,Driver
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q,Sum,F
from datetime import datetime
from django.http import HttpResponse,Http404




UserModel = get_user_model()

class IsUnauthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated

class UserRegister(APIView):
    permission_classes = [IsUnauthenticated]
    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [IsUnauthenticated]
    authentication_classes = (SessionAuthentication,)
    ##
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    ##
    def get(self, request):
        trips = Trip.objects.filter(Q(departure_time__gte=datetime.now()) | Q(driver__car_space__gte=F('space_left')) | Q(space_left__lte=5000))
        trip_serializer = TripSerializer(trips,many=True)
        my_trips = Booking.objects.filter(passenger=request.user.pk)
        serializer = UserSerializer(request.user)
        
        
        mytrip_serializer = BookingSerializer(my_trips)
        response_data = {
            "trips":trip_serializer.data,
            "user":serializer.data,
            "mytrip":mytrip_serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

class AllTrips(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def get(self,request):
        trips = Trip.objects.filter(Q(departure_time__gte=datetime.now()) | Q(driver__car_space__gte=F('space_left')) | Q(space_left__lte=5000))
        serializer = TripSerializer(trips,many=True)
        user = UserSerializer(request.user)
        response_data = {
            "trips":serializer.data,
            "user":user.data
        }
        return Response(response_data)

class CreateTrip(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request):
        #users = AppUser.objects.all()
        serializer = TripSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            "trip":serializer.data,
        }
            return Response(response_data)
        else:
            print(serializer.errors)


class RegisterDriver(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request):
        request.data['user'] = request.user.pk
        user = get_object_or_404(UserModel,pk=request.user.pk)
        user.user_type = "driver"
        user.save()
        print(user.user_type)
        serializer = DriverSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response_data = {
            "driver":serializer.data,
        }
            return Response(response_data)
        else:
            print(serializer.errors)
    
class AcceptDrive(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request,tripid):
        if request.user.user_type=="driver":
            driver = get_object_or_404(Driver,user=request.user.pk)
            trip = get_object_or_404(Trip,pk=tripid)

            if trip.driver is None:
                current_space = Booking.objects.filter(trip=trip).aggregate(used_space=Sum('cargo_size'))['used_space']
                trip.driver = driver
                trip.space_left = trip.driver.car_space - current_space
                trip.save()
            else:
                return Response({"error":"Driver already exists"})
            
        return Response("success")
    
class UnAcceptDrive(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request,tripid):
        if request.user.user_type=="driver":
            driver = get_object_or_404(Driver,user=request.user.pk)
            trip = get_object_or_404(Trip,driver=driver)

            if trip.driver:
                current_space = Booking.objects.filter(trip=trip).aggregate(used_space=Sum('cargo_size'))['used_space']
                trip.driver = None
                #trip.space_left = trip.driver.car_space - current_space
                trip.save()
            
                return Response("success")
        
    

class BookTrip(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request):
        request.data['passenger'] = request.user.pk
        #request.data['trip'] = request.POST.get('')
        serializer = BookingSerializer(data=request.data)
        user = UserSerializer(request.user)
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            "bookings":serializer.data,
            "user":user.data
            }
            return Response(response_data)
        

class DriverDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    
    def get(self,request):
        trips = Trip.objects.all()[0:4]
        my_trips = Booking.objects.filter(passenger=request.user.pk)
        my_bookings = BookingSerializer(my_trips,many=True)
        serializer = TripSerializer(trips,many=True)
        user = UserSerializer(request.user)
        
        response_data = {
            "my_trips":my_bookings.data,
            "trips": serializer.data,
            "user":user
        }
        return Response(response_data)
        

class MyTrips(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    
    def get(self,request):
        my_trips = Booking.objects.filter(passenger=request.user.pk)
        user = UserSerializer(request.user)
        serializer = BookingSerializer(my_trips,many=True)
        response_data = {
            "my_trips":serializer.data,
            "user":user.data
            
        }
        return Response(response_data)


class DriverDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    ##
    def get(self, request):
       
        if request.user.user_type=="driver":
            trips = Trip.objects.filter(Q(departure_time__gte=datetime.now()) |Q(driver=None)| Q(driver__car_space__gte=F('space_left')) | Q(space_left__lte=5000))[0:4]
            serializer =  serializer = TripSerializer(trips,many=True)
            user = UserSerializer(request.user)
            response_data = {
                "trips":serializer.data,
                "user":user.data
            
            }
            
            return Response(response_data, status=status.HTTP_200_OK)

class CancelTrip(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request,tripid):
        try:
            booking = get_object_or_404(Booking,trip=tripid)
            booking.delete()
            return HttpResponse("Object deleted successfully")
        except Http404:
            return HttpResponse("Object not found", status=404)

class EndTrip(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request,tripid):
        if request.user.user_type == "driver":
            
            try:
                trip = get_object_or_404(Trip,pk=tripid)
                trip.driver = None
                trip.save()
                return HttpResponse("Trip ended successfully")
            except Http404:
                return HttpResponse("Object not found", status=404)
                
class TripDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def get(self,request,tripid):
            try:
                trip = get_object_or_404(Trip,pk=tripid)
                serializer = TripSerializer(trip)
                return Response(serializer.data)
            except Http404:
                return HttpResponse("Object not found", status=404)


        
