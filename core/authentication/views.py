from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer, RegisterSerializer,UserTokenSerializer
from .messages.responses_ok import LOGIN_OK, SIGNUP_OK
from .messages.responses_error import LOGIN_CREDENTIALS_REQUIRED_ERROR, LOGIN_CREDENTIALS_ERROR

# Create your views here.
class LoginView(generics.GenericAPIView):
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
    def get(self, request):
        try:
            token_r = request.GET.get('token')
            token = Token.objects.all()
            for tk in token:
                print(tk)
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expired_date__gte=datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                token.delete()
                session_message = 'Sesiones de usuarios eliminados'
                token_message = 'Token eliminado'
                return Response({"token_msg":token_message,"Session_msg":session_message},status=status.HTTP_200_OK)
            return Response({"Error":"Campos no encontrados"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error:":"No se encuentra ningun usuario con esas credenciales"}, status=status.HTTP_409_CONFLICT)
  

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
