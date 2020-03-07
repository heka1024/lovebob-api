from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import *
from .models import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('time')
    serializer_class = MenuSerializer

    def get_queryset(self):
        _date = self.request.query_params.get('date')
        if _date == None:
            queryset = Menu.objects.all().order_by('time')
        else:
            queryset = Menu.objects.all().filter(date = _date).order_by('time')
        
        return queryset
    
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer