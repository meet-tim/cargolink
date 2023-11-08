from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer,TripSerializer,BookingSerializer
from rest_framework import permissions, status
from .validations import custom_validation, validate_email, validate_password
from .models import Trip,AppUser,Booking

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
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class AllTrips(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def get(self,request):
        trips = Trip.objects.all()
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
            print(serializer.errors)
            print("blank")
            response_data = {
            "trip":serializer.data,
        }
            return Response(response_data)
        else:
            print(serializer.errors)
       
class BookTrip(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
 
    def post(self,request):
        print(request.user.pk)
        request.data['passenger'] = request.user.pk
        request.data[""]
        #request.data['trip'] = request.params.trip
        serializer = BookingSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            response_data = {
            "bookings":serializer.data,
            }
            return Response(response_data)
        

class Dashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    
    def get(self,request):
        trips = Trip.objects.all()[0:4]
        my_trips = Booking.objects.filter(passenger=request.user.pk)
        my_bookings = BookingSerializer(my_trips,many=True)
        serializer = TripSerializer(trips,many=True)
        response_data = {
        "my_trips":my_bookings.data,
        "trips": serializer.data
        }
        return Response(response_data)
        

class MyTrips(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    
    def get(self,request):
        my_trips = Booking.objects.filter(passenger=request.user.pk)
        
        serializer = BookingSerializer(my_trips,many=True)
        response_data = {
            "my_trips":my_trips,
        }
        return Response(response_data)