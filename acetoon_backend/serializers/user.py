from rest_framework import serializers
from acetoon_backend.models import User, Organizer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creation and modification of profile
    """
    class Meta:
        model = User
        read_only_fields = ['username', ]
        exclude = ['groups', 'user_permissions',
                   'is_staff', 'is_superuser', 'is_active',
                   'password']


class UserNavSerializer(serializers.ModelSerializer):
    """
    Serializers for Navigation Bar
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'profile_pic')


class OrganizerSerializer(serializers.ModelSerializer):
    """
    Serializer for Organizer Creation
    """

    class Meta:
        model = Organizer
        read_only_fields = ('user', 'is_organizer')
        fields = '__all__'
