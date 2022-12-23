from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from core.settings import EMAIL_HOST_USER

from .models import CustomUser,CodesVerification
from .serializers import UserSerializer, RegisterSerializer,UserTokenSerializer,LoginSerializer, ValidateCodeSerializer
from .messages.responses_ok import CODE_VALIDATED, DELETED_USER, EMAIL_SEND, LOGIN_OK, PASSWORD_CHANGED, SIGNUP_OK,LOGOUT_OK, UPDATE_OK
from .messages.responses_error import CHANGED_PASSWORD_ERROR, CODER_VERIFICATION_ERROR, LOGIN_CREDENTIALS_REQUIRED_ERROR, LOGIN_CREDENTIALS_ERROR,LOGOUT_ERROR, NOT_FOUND_USER
from .helpers.content_emails import PASSWORD_RESET
from .helpers.randCodes import generatedCode
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
            
            return Response(LOGOUT_OK,status=status.HTTP_200_OK)
        return Response(LOGOUT_ERROR, status=status.HTTP_400_BAD_REQUEST)      

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
        status=status.HTTP_200_OK)

class UpdateUser(generics.RetrieveUpdateAPIView):
    
    serializer_class = UserTokenSerializer
    queryset = CustomUser.objects.all()

    def put(self, request, *args, **kwargs):

        return Response({
            'data':request.data,
            'message':UPDATE_OK
        },status=status.HTTP_202_ACCEPTED)


class ListUsers(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.order_by('id')

class DeleteView(generics.GenericAPIView):
    
    def delete(self, request, pk):
        user= CustomUser.objects.get(id=pk)
        if user:
            user.delete()
            return Response(DELETED_USER, status=status.HTTP_200_OK)
        else:
            return Response(NOT_FOUND_USER, status=status.HTTP_404_NOT_FOUND)

class SendCodeResetPassword(generics.GenericAPIView):

    def post(self,request):
        email = request.data.get('email',None)
        try:
            user = CustomUser.objects.get(email=email)
            if user:
                mailReset = EmailMultiAlternatives(
                    'Reset password',
                    'Syncronik Interships',
                    EMAIL_HOST_USER,
                    [email]

                )
                
                code = CodesVerification(
                    changePasswordCode=generatedCode(),
                    user = user
                )
                code.save()

                mailReset.attach_alternative(f'<h1>Your verification Code: {code.changePasswordCode}</h1>','text/html')
                mailReset.send()

                return Response(EMAIL_SEND,status=status.HTTP_200_OK)
        except:
            return Response(LOGIN_CREDENTIALS_ERROR, status=status.HTTP_401_UNAUTHORIZED)

class ValidationCodeView(generics.GenericAPIView):
    def post(self,request):
        code_request = request.data.get('code',None)
        try:
            code_database = CodesVerification.objects.get(changePasswordCode=code_request)
            serializerValidate = ValidateCodeSerializer(code_database)
            if code_database is not None:
                return Response({
                    'Validated':CODE_VALIDATED,
                    'Entity':serializerValidate.data,
                    },status=status.HTTP_202_ACCEPTED)
        except:
            return Response(CODER_VERIFICATION_ERROR, status=status.HTTP_401_UNAUTHORIZED)

class ResetPasswordView(generics.GenericAPIView):
    def post(self,request):
        userId = request.data.get('user',None)
        new_password = request.data.get('password',None)
        if new_password is not None and userId is not None:
            user = CustomUser.objects.get(id=userId)
            user.set_password(new_password)
            user.save()
            return Response(PASSWORD_CHANGED,status=status.HTTP_200_OK)
        else:
            return Response(CHANGED_PASSWORD_ERROR,status=status.HTTP_400_BAD_REQUEST)