from django.urls import include, path, re_path
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'menus', views.MenuViewSet)
router.register(r'comments', views.CommentView)
router.register(r'restaurants', views.RestaurantViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'comment_new/<int:no>/', views.comment_new, name = 'comment_new'),
    path(r'comment_delete/<int:pk>/', views.comment_delete, name = 'comment_delete'),
    re_path(r'restaurant/(?P<no>\d+)/$', views.RestaurantDetail, name='restaurant-detail'),
    # re_path(r'comment_pnew/(?P<no>\d+)/$', views.CommentCreate.as_view())
    
]