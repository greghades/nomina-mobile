from rest_framework import serializers
from .models import CustomUser,CodesVerification



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username', 'email','first_name', 'last_name')

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','password')
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username = validated_data['email'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'])
        return user

class ValidateCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodesVerification
        exclude = ('id',)
