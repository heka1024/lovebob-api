from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from quickstart.serializers import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('time')
    serializer_class = MenuSerializer
    
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
RestaurantDetail = RestaurantViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})
    
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    
class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    
    
@login_required
@api_view(['GET', 'POST'])
def comment_new(request, no = 18):
    if request.method == "POST":
        author = request.user
        restaurant = Restaurant.objects.get(id = no)
        text = request.data.get('text', '잘못된 입력입니다.')
        pnew = Comment(
            author = author,
            restaurant = restaurant,
            text = text
        )
        pnew.save()
        return Response('{data: good}')
    else:
        restaurant = Restaurant.objects.get(id = no)
        print(restaurant)
        return Response('{data: login_required}')
    
@login_required
@api_view(['GET', 'POST'])
def comment_delete(request, pk):
    if request.method == "POST":
        want_to_delete = Comment.objects.get(pk = pk)
        want_to_delete.delete()
        return Response('{data: success}')
    else:
        return Response('{data: fail}')