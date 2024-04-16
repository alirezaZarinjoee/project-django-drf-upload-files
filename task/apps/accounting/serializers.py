from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'repassword']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['repassword']:
            raise ValidationError("Password and repassword are not the same")
        return data

    def create(self, validated_data):
        del validated_data['repassword']
        return CustomUser.objects.creat_user(**validated_data)
        