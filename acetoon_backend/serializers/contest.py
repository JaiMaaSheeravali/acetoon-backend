from rest_framework import serializers
from acetoon_backend.models import Contest


class ContestListSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Contests List
    """
    organizer = serializers.SerializerMethodField('get_organizer')

    class Meta:
        model = Contest
        exclude = ('rules', 'prizes', 'eligibility')

    def get_organizer(self, obj):

        organizer = obj.organizer
        return organizer.user.username


class ContestDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Contest details
    """

    class Meta:
        depth = 1
        model = Contest
        exclude = ('rules',)


class ContestRulesSerializer(serializers.ModelSerializer):
    """
    Serializer for Rules Page
    """

    class Meta:
        model = Contest
        fields = ('id', 'name', 'rules',)


class ContestCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creation of competition
    """

    class Meta:
        model = Contest
        read_only_fields = ['organizer', ]
        fields = '__all__'
