from django.db import models
from django.urls import reverse 
import uuid
from django.contrib.auth.models import User

from datetime import datetime

class Restaurant(models.Model):
    name = models.CharField(max_length = 100, help_text = '식당의 이름')
    number = models.CharField(max_length = 20, help_text = '식당의 전화번호')
    location = models.CharField(max_length = 50, help_text = '식당의 위치')
    lng = models.FloatField(help_text = '식당의 경도')
    lat = models.FloatField(help_text = '식당의 위도')
    
    likes = models.ManyToManyField(User, blank = True, related_name = 'like_users')
    
    def get_menus(self, date_q, time_q):
        return self.menus.filter(date = date_q, time = time_q)
        
    def __str__(self):
        return f'{self.name}, {self.number}'
    
    def get_absolute_url(self):
        return reverse('restaurant_detail', args=[str(self.id)])
    
class Menu(models.Model):
    name = models.CharField(max_length = 100, help_text = '메뉴의 이름')
    price = models.IntegerField(default = 0)
    date = models.DateField(null = True, blank = True)
    restaurant = models.ForeignKey(Restaurant, related_name = 'menus', on_delete = models.SET_NULL, null = True)
    rname = models.CharField(max_length = 100, help_text = '레스토랑 이름')
    
    TIME = (
        ('b', '아침'),
        ('l', '점심'),
        ('d', '저녁'),
        ('n', '정보 없음'),
    )
    
    time = models.CharField(
        max_length = 1,
        choices = TIME,
        blank = True,
        default = 'n',
        help_text ='제공 시간',
    )

    def __str__(self):
        return f'{self.name}, {self.price}, {self.date}, ({self.restaurant})'
    
class Comment(models.Model):
    author = models.ForeignKey(User, null =True, on_delete=models.SET_NULL)
    restaurant = models.ForeignKey(Restaurant, null =True, related_name = "comments", on_delete=models.SET_NULL)
    text = models.TextField()
    created_at = models.DateTimeField(default = datetime.now())
    
    class Meta():
        ordering = ['-created_at']

    def time(self):
        return self.created_at.isoformat()[:10]
    
    def __str__(self):
        return f'{self.author}, {self.created_at}, {self.text}'


    