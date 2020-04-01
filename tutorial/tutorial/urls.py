from django.urls import include, path, re_path
from django.conf.urls import url
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
router.register(r'apiusers', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'menus', views.MenuViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'restaurants', views.RestaurantViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

lists = [
    path(r'comment_new/<int:no>/', views.comment_new, name = 'comment_new'),
    path(r'comment_delete/<int:pk>/', views.comment_delete, name = 'comment_delete'),
    path(r'like/<int:pk>/', views.like, name = 'toggle-like'),
    re_path(r'restaurant/(?P<no>\d+)/$', views.RestaurantDetail, name='restaurant-detail'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]
urlpatterns = [
  path('api/', include(router.urls)),
  url(r'^api/', include(lists))
]