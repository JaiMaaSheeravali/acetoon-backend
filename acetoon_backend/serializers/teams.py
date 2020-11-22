from rest_framework import serializers
from acetoon_backend.models import Team
from acetoon_backend.serializers.user import UserNavSerializer


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for Creating Team
    """

    class Meta:
        model = Team
        read_only_fields = ('owner', 'token')
        exclude = ('members', )


class TeamDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Team Details
    """

    owner = UserNavSerializer()
    members = UserNavSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'owner', 'members', 'name']
