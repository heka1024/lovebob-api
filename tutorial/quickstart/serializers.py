from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        
class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    liked = UserSerializer(source='likes', many=True)
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'number', 'location', 'lng', 'lat', 'liked']
        
class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.CharField(source='author.username')
    res = RestaurantSerializer(source='restaurant')

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'res', 'text', 'created_at']
        
class MenuSerializer(serializers.HyperlinkedModelSerializer):
    res_id = serializers.CharField(source='restaurant.id')
    
    class Meta:
        model = Menu
        fields = ['name', 'price', 'date', 'restaurant', 'res_id', 'time', 'rname']