from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout

from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer,UserTokenSerializer,LoginSerializer
from .messages.responses_ok import LOGIN_OK, SIGNUP_OK,LOGOUT_OK, UPDATE_OK
from .messages.responses_error import LOGIN_CREDENTIALS_REQUIRED_ERROR, LOGIN_CREDENTIALS_ERROR,LOGOUT_ERROR

# Create your views here.
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def get(self, request):
        data_response = {"msg": "Método GET no permitido"}
        return Response(data_response, status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
    
        if email is None or password is None:
            return Response(LOGIN_CREDENTIALS_REQUIRED_ERROR, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(email = email, password = password)

            if user is not None: 
                if user.is_active:
                    token,create = Token.objects.get_or_create(user=user)
                    rspn = {
                        "Token":token.key,
                        "user": UserTokenSerializer(user, context = self.get_serializer_context()).data,
                        "message": LOGIN_OK
                    }
                    if create:
                        return Response( rspn, status=status.HTTP_200_OK)
                    else:
                        token.delete()
                        token = Token.objects.create(user=user)
                        return Response( rspn, status=status.HTTP_200_OK)
            else:
                return Response(LOGIN_CREDENTIALS_ERROR, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
    
    def post(self, request):
        token_request = request.data.get("Token", None)
        print(token_request)
        token = Token.objects.get(key=token_request)
        if token:
            user = CustomUser.objects.get(auth_token=token)
            user.auth_token.delete()
            logout(request)
            
            return Response({"message":LOGOUT_OK},status=status.HTTP_200_OK)
        return Response({"message":LOGOUT_ERROR}, status=status.HTTP_400_BAD_REQUEST)      

class SignUpView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context = self.get_serializer_context()).data,
                "message": SIGNUP_OK
            },
        )

class UpdateUser(generics.RetrieveUpdateAPIView):
    
    serializer_class = UserTokenSerializer
    queryset = CustomUser.objects.all()

    def put(self, request, *args, **kwargs):

        return Response({
            'data':request.data,
            'message':UPDATE_OK
        })


class ListUsers(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.order_by('id')

