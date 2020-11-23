from rest_framework import serializers
from acetoon_backend.models import Submission


class SubmissionListSerializer(serializers.ModelSerializer):
    """
    Serializer to show list of Submissions of a contest
    """
    name = serializers.SerializerMethodField('get_team')

    class Meta:
        model = Submission
        fields = ('id', 'name', 'team', 'timestamp')

    def get_team(self, obj):

        team = obj.team
        return team.name


class SubmissionDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Detailed Submission
    """

    class Meta:
        model = Submission
        fields = '__all__'


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for Detailed Submission
    """

    class Meta:
        model = Submission
        read_only_fields = ('team', 'contest')
        fields = '__all__'
