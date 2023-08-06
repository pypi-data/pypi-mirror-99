from rest_framework import serializers, generics, permissions, status
from authapi.models import *
from rest_framework.serializers import ModelSerializer


from rest_framework import serializers
from django.contrib.auth import authenticate

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('email','password')

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
        

    def create(self, validated_data):
        
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone = validated_data['phone'],
            is_active = True,
            adresse = validated_data['adresse']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserRegisterSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        depth = 1
        

    def create(self, validated_data):
        
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active = True,
        )
        user.set_password("socialdatabase")
        user.save()
        return user

class UserRegisterLivreurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1
        

    def create(self, validated_data):
        
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone = validated_data['phone'],
            is_active = True,
            adresse = validated_data['adresse'],
            user_type = "livreur"
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_active', 'is_staff')

    def create(self, validated_data, **extra_fields):
        user = self.Meta.model(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordResetSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    class Meta:
        model = PasswordReset
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class RequestPasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    email = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    code = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
