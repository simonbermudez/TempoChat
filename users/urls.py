from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, user_signup, user_login, user_logout

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'), 
]