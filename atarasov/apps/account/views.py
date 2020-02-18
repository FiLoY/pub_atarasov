from django.conf import settings
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as DjangoLoginView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import ObtainJSONWebToken

from .models import User
from .serializers import UserSerializer
from .forms import SignUpForm


class Login(DjangoLoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class SignUp(DjangoLoginView):
    form_class = SignUpForm
    template_name = 'account/signup.html'
    redirect_authenticated_user = True


    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend=settings.AUTHENTICATION_BACKENDS[1])
        return redirect('/')


# -------------------------------------------------------------- #
# API                                                            #
# -------------------------------------------------------------- #
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def retrieve(self, request, *args, **kwargs):
        print(request.user)
        return super().retrieve(request, *args, **kwargs)

#
class GetUserViewSet(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"user": serializer.data})


class SignUpViewSet(ObtainJSONWebToken):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = {'errors': []}

        try:
            validate_email(request.data.get('email'))
            print(request.data.get('email'))
        except Exception:
            data['errors'] += ['Некорректная почта.']


        try:
            User.objects.get(username__iexact=request.data.get('username'))
        except ObjectDoesNotExist:
            pass
        else:
            data['errors'] += ['Пользователь с таким именем уже существует']

        try:
            User.objects.get(email__iexact=request.data.get('email'))
        except ObjectDoesNotExist:
            pass
        else:
            data['errors'] += ['Пользователь с такой почтой уже существует']

        if not data['errors']:
            u = User.objects.create_user(username=request.data.get('username'),
                                     email=request.data.get('email'),
                                     password=request.data.get('password'))
            data['errors'] += [f'{u.username}']


            return super().post(request, *args, **kwargs)
        else:
            return Response(data)