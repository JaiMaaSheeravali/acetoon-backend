from rest_framework import serializers
from acetoon_backend.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for modify and display  profile
    """
    class Meta:
        model = User
        read_only_fields = [
            'username',
        ]
        fields = '__all__'


class UserNavSerializer(serializers.ModelSerializer):
    """
    Serializers for Navigation Bar
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_pic')
