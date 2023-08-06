# -*- coding: utf-8 -*-

# Create your views here.
from django.core.exceptions import ViewDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from api.models import *
from api.serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
#login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login

#from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.views import ObtainAuthToken
import datetime, random, string
import csv, io
from django.shortcuts import render
from django.contrib import messages
import json
from django.core.mail import EmailMultiAlternatives, send_mail

from api.utils import Utils as my_utils
from fpdf import FPDF, HTMLMixin
from django.template.loader import get_template, render_to_string

from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa 
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_jwt.settings import api_settings

from datetime import datetime, timedelta
from django.utils.timezone import now  
from dateutil import relativedelta
# import numpy as np
import uuid



jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



N = 7


def get_random():
        # return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
        return ''.join(random.SystemRandom().choice(string.digits) for _ in range(N))

def get_code():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

class LoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=result.data['token'])
        update_last_login(None, token.user)
        return result

class UserRegisterView(generics.CreateAPIView):
    
    permission_classes = (
    )
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
       
        serializer = UserRegisterSerializer(data=request.data)
       
        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({
            "status": "success",
            "message": "item successfully created",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class UserRegisterSocialView(generics.CreateAPIView):
    
    permission_classes = (
    )
    queryset = User.objects.all()
    serializer_class = UserRegisterSocialSerializer

    def post(self, request, *args, **kwargs):
       try:
            item = User.objects.get(email=request.data['email'])
          
            payload = jwt_payload_handler(item)
            
            token = jwt_encode_handler(payload)
            
            return Response({'token': token}, status=status.HTTP_200_OK)
       except User.DoesNotExist:
            serializer = UserRegisterSocialSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    "status": "failure",
                    "message": "invalid data",
                    "error": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                "status": "success",
                "message": "item successfully created",
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)


class GoogleView(generics.CreateAPIView):
    
    permission_classes = (
    )
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            item = User.objects.get(email=request.data['email'])
          
            payload = jwt_payload_handler(item)
            
            token = jwt_encode_handler(payload)
            
            return Response({
            'token': token
        }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=404)

class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
            serializer = UserSerializer(item)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        self.data = request.data.copy()
        if 'password' in request.data :
                item.set_password(request.data['password'])
                self.data['password']  = item.password

                
        serializer = UserSerializer(item, data= self.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)

class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
  

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)

        if not user:
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UserSerializer(user).data

        return Response({
            "status": "success",
            "message": "item successfully created",
            "data": data
        }, status=status.HTTP_200_OK)

class UserAPIListView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, format=None):
        items = User.objects.order_by('pk')
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class PasswordResetView(generics.CreateAPIView):
    """ use postman to test give 4 fields new_password  new_password_confirm email code post methode"""
    permission_classes = (
        
    )
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):

        if 'code' not in request.data or request.data['code'] is None:
            return Response({
                "status": "failure",
                "message": "no code provided",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        if 'email' not in request.data or request.data['email'] is None:
            return Response({
                "status": "failure",
                "message": "no email provided",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        if'new_password' not in request.data or 'new_password_confirm' not in request.data or request.data['new_password'] is None or request.data['new_password'] != request.data['new_password_confirm']:
            return Response({
                "status": "failure",
                "message": "non matching passwords",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_ = User.objects.get(email=request.data['email'])
            code_ = request.data['code']
            if user_ is None:
                return Response({
                    "status": "failure",
                    "message": "no such item",
                    "error": "not such item"
                }, status=status.HTTP_400_BAD_REQUEST)

            passReset = PasswordReset.objects.filter(
                user=user_, code=code_, used=False).order_by('-date_created').first()
            # print(passReset)
            if passReset is None:
                return Response({
                    "status": "failure",
                    "message": "not such item",
                    "error": "not such item"
                }, status=status.HTTP_400_BAD_REQUEST)

            user_.set_password(request.data['new_password'])
            user_.save()
            passReset.used = True
            passReset.date_used = timezone.now()
            passReset.save()

            
        except User.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "invalid data",
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                "status": "success",
                "message": "item successfully saved",
            }, status=status.HTTP_201_CREATED)

class PasswordResetRequestView(generics.CreateAPIView):
    """ use postman to test give field email post methode"""
    permission_classes = (
        
    )
    queryset = User.objects.all()
    serializer_class = RequestPasswordSerializer

    def post(self, request, *args, **kwargs):

        # get user using email
        # if user

        if 'email' not in request.data or request.data['email'] is None:
            return Response({
                "status": "failure",
                "message": "no email provided",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_ = User.objects.get(email=request.data['email'])
            # generate random code
            code_ = get_random()
            # crete and save pr object
            PasswordReset.objects.create(
                user=user_,
                code=code_
            )

            
            subject = 'Réinitialisation mot de passe'
            message = " Vous avez oublié votre mot de passe ? Pas de panique!  Vous pouvez le réinitialiser en utilisant le code suivant  et en indiquant votre nouveau mot de passe. "+code_
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_.email,]
            send_mail( subject, message, email_from, recipient_list )    
        
        except User.DoesNotExist:
            # print('sen error mail')
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)


        return Response({
            "status": "success",
            "message": "item successfully saved ",
        }, status=status.HTTP_201_CREATED)

class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (permissions.IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.password_reset_count = 1
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
