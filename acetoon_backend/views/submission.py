from rest_framework.response import Response
from rest_framework.decorators import action
from acetoon_backend.models import Submission, Contest, Team
from rest_framework import viewsets, status
from acetoon_backend.serializers import (
    SubmissionListSerializer,
    SubmissionDetailSerializer,
    SubmissionCreateSerializer
)
from rest_framework.permissions import IsAuthenticated
from acetoon_backend.permissions import IsOrganizer


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    View to Get submission
    """

    permission_classes = [IsAuthenticated, IsOrganizer]

    def get_queryset(self):

        contest_id = self.request.query_params.get('contest_id', None)
        user = self.request.user.user
        queryset = Submission.objects.none()

        if contest_id is not None:
            contest = Contest.objects.get(id=contest_id)
            if user.id == contest.organizer.id:
                queryset = contest.submissions.all()

        else:
            queryset = Submission.objects.none()

        return queryset

    def get_serializer_class(self):

        if self.action == 'list':
            return SubmissionListSerializer
        elif self.action == 'retrieve':
            return SubmissionDetailSerializer
        else:
            return SubmissionCreateSerializer

    def create(self, request, *args, **kwargs):

        contest_id = self.request.query_params.get('contest_id', None)
        data = self.request.data

        try:
            contest = Contest.objects.get(id=contest_id)

        except Contest.DoesNotExist:
            return Response(
                data='No such Contest Exists',
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = data['token']
            team = Team.objects.get(token=token, contest=contest_id)

        except Team.DoesNotExist:
            return Response(
                data='No such Team Exist',
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SubmissionCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save(team=team, contest=contest)
            data = 'Submitted Successfully'

            return Response(
                data=data,
                status=status.HTTP_201_CREATED
            )
        else:
            print(serializer.errors)

            return Response(
                data='Unable to Create Team',
                status=status.HTTP_400_BAD_REQUEST
            )
