from rest_framework import serializers
from acetoon_backend.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creation and modification of profile
    """
    class Meta:
        model = User
        read_only_fields = ['username', ]
        exclude = ['groups', 'user_permissions']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UserNavSerializer(serializers.ModelSerializer):
    """
    Serializers for Navigation Bar
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_pic')

