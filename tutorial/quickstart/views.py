from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from quickstart.serializers import *
from .models import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    
    def get_serializer_class(self):
      return CommentSerializer

    def get_queryset(self):
        _id = self.request.query_params.get('id')
        if _id == None:
            queryset = Comment.objects.order_by('created_at')
        else:
            queryset = Comment.objects.all().filter(restaurant__id = _id).order_by('created_at')
        
        return queryset
    
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
    
RestaurantDetail = RestaurantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def comment_new(request, no = 18):
    if request.method == "POST":
        author = request.user
        restaurant = Restaurant.objects.get(id = no)
        text = request.data.get('text', '')
        if text == '':
          return Response({'result': 'fail to create'}, status = status.HTTP_400_BAD_REQUEST)
        pnew = Comment(
            author = author,
            restaurant = restaurant,
            text = text
        )
        pnew.save()
        return Response({'result': 'success'}, status = status.HTTP_201_CREATED)
    else:
        restaurant = Restaurant.objects.get(id = no)
        print(restaurant)
        return Response({'result': 'post required'})
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def comment_delete(request, pk):
    if request.method == "POST":
        want_to_delete = Comment.objects.get(pk = pk)
        want_to_delete.delete()
        return Response({'result': 'success'}, status = status.HTTP_202_ACCEPTED)
    else:
        return Response({'result': 'post required'}, status = status.HTTP_400_BAD_REQUEST)
      
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def like(request, pk):
    print('like is called')
    user = request.user
    print(user)
    restaurant = Restaurant.objects.get(pk = pk)

    if restaurant.likes.filter(username = user.username).exists():
        restaurant.likes.remove(user)    
        return Response({'result': 'success to remove like'}, status = status.HTTP_202_ACCEPTED)
    else:
        restaurant.likes.add(user)
        return Response({'result': 'success to add like'}, status = status.HTTP_202_ACCEPTED)