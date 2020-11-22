import hashlib
from acetoon_backend.models import Team, Contest, User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from acetoon_backend.serializers import TeamSerializer, TeamDetailSerializer
from django.core.mail import EmailMessage
from rest_framework.response import Response
from rest_framework.decorators import action


def send_email(response):
    """
    Function to facilitate Email Service
    """
    contest_id = response['contest']
    contest_name = Contest.objects.get(id=contest_id).name
    token = response['token']
    email_id = response['email']
    receivers = [email_id, ]
    email = EmailMessage(
        'Acetoon Team Registration',
        ('Thank You :) for your Registration with Acetoon in ' + contest_name + '. Your Token for invitation is:  '
         + token),
        'acetoon.help.info@gmail.com',
        receivers
    )

    email.send()


class TeamCreateViewSet(viewsets.ModelViewSet):
    """
    View to Create Team
    """

    http_method_names = ['post', 'get', 'patch']
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        """
        Endpoint to create a team based
        """
        data = self.request.data
        print(data)
        token = str(data['contest']) + str(self.request.user)
        token = hashlib.sha256(token.encode())
        token = token.hexdigest()
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user, token=token, )
            print(serializer.data)
            send_email(serializer.data)  # sending mail
            data = 'Created Team Successfully'

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

    @action(
        methods=['PATCH', 'GET'],
        detail=False,
        url_name='join',
        url_path='join',
    )
    def join_team(self, request):

        if request.method == 'PATCH':
            """
            Endpoint to Join a existing team
            """
            data = self.request.data
            token = data['token']
            contest_id = data['contest']
            try:
                print(data['token'])
                team = Team.objects.get(token=token)
                team.members.add(self.request.user)
                team.save()
                data = 'Member added Successfully'

                return Response(
                    data=data,
                    status=status.HTTP_202_ACCEPTED
                )

            except Team.DoesNotExist:
                data = 'No such Team exist'

                return Response(
                    data=data,
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'GET':
            """
            Display teams for a contest
            : requires a GET parameter as contest_id
            """
            contests_id = self.request.query_params.get('contest_id')
            contests = Contest.objects.get(id=contests_id)
            teams = contests.participants.all()
            serializer = TeamDetailSerializer(teams, many=True)

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
