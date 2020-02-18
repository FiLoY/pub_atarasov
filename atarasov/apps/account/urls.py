from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter
from .views import Login, SignUp


urlpatterns = [
    path('signin/', Login.as_view(), name='signin'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signout/', LogoutView.as_view(), name='signout'),

]