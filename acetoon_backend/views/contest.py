from acetoon_backend.models import Contest, Announcement
from acetoon_backend.serializers import (
    ContestListSerializer,
    ContestDetailSerializer,
    ContestRulesSerializer,
    ContestCreateSerializer,
    AnnouncementSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from acetoon_backend.permissions import IsOrganizer, AnnouncementPermission
from itertools import chain


class ContestDetail(viewsets.ModelViewSet):

    """
    View to Return Contest Detail
    """

    permission_classes = [IsAuthenticated, ]
    http_method_names = ['get']
    queryset = Contest.objects.all()

    def get_serializer_class(self):
        """
        This function decides the serializer class according to the type of
        request
        :return: the serializer class
        """

        if self.action == 'list':
            return ContestListSerializer
        elif self.action == 'retrieve':
            return ContestDetailSerializer

    @action(
        detail=False,
        methods=['GET'],
        url_name='rules',
        url_path='rules'
    )
    def rules(self, request):

        contest_id = self.request.query_params.get('id', None)

        if contest_id is not None:
            contest = Contest.objects.get(id=contest_id)
            serializer = ContestRulesSerializer(contest)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            data = 'Not Found'
            return Response(
                data=data,
                status=status.HTTP_404_NOT_FOUND
            )

    @action(
        detail=False,
        url_name='my_contests',
        url_path='my_contests',
        methods=['GET']
    )
    def my_contests(self, request):
        """
        Views to return My Contests
        """
        user = self.request.user
        contests_team_member = Contest.objects.filter(
            participants__members__username=user
        )
        contest_team_owner = Contest.objects.filter(
            participants__owner=user
        )
        if hasattr(user, 'user'):

            contest_owner = Contest.objects.filter(
                organizer=user.user
            )

            result_list = list(chain(
                contest_owner,
                contest_team_owner,
                contests_team_member
            ))

        else:
            result_list = list(chain(
                contest_team_owner,
                contests_team_member
            ))

        res_list = []
        for i in result_list:
            if i not in res_list:
                res_list.append(i)

        serializer = ContestListSerializer(res_list, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


class ContestCreate(viewsets.ModelViewSet):
    """
    View for creation of Contest
    """

    permission_classes = [IsOrganizer, ]
    http_method_names = ['post', ]
    serializer_class = ContestCreateSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user.user)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    View for Announcements of a Contest
    """

    http_method_names = ['post', 'get']
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated & AnnouncementPermission]
    lookup_field = 'contest'
    queryset = Announcement.objects.all()

    def get_queryset(self):

        contest_id = self.request.query_params.get('contest_id', None)
        user = self.request.user.user

        if contest_id is not None:
            contest = Contest.objects.get(id=contest_id)
            queryset = contest.announcements.all()

        else:
            queryset = Announcement.objects.none()

        return queryset

    def perform_create(self, serializer):

        contest_id = self.request.query_params.get('contest_id', None)
        contest = Contest.objects.get(id=contest_id)

        if contest_id is not None:
            serializer.save(contest=contest)
