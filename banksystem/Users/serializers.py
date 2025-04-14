from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'kyc_verified')
        extra_kwargs = {
            'password': {'write_only': True},
            'kyc_verified': {'read_only': True}
        }