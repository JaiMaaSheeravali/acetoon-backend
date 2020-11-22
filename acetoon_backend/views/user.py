from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate

from acetoon_backend.serializers import UserNavSerializer, UserSerializer
from acetoon_backend.models import User
from acetoon_backend.permissions import AdminOnlyPermissions, IsOwnerOrAdmin


class UserNavView(viewsets.ReadOnlyModelViewSet):
    """
    Return the user details for Navigation bar
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserNavSerializer

    def get_queryset(self):

        user = User.objects.get(id=self.request.user.id)
        queryset = User.objects.filter(username=user)
        return queryset


class UserCreateViewSet(viewsets.ModelViewSet):
    """
    Allows creations of User and Display list of User
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnlyPermissions, ]

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_name='who_am_i',
        url_path='who_am_i',
        permission_classes=[IsOwnerOrAdmin],
    )
    def who_am_i(self, request):
        """
        endpoint for updating of profile and get details of logged in User
        """

        if request.method == 'PATCH':
            data = self.request.data

            user = User.objects.get(id=self.request.user.id)

            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

            data = 'Update Successfully'
            return Response(
                data=data,
                status=status.HTTP_201_CREATED
            )

        elif request.method == 'GET':

            user_id = self.request.user.id
            user = User.objects.get(id=user_id)
            data = UserSerializer(user).data

            return Response(
                data=data,
                status=status.HTTP_200_OK
            )

    @action(
        methods=['POST', ],
        detail=False,
        url_name='onlogin',
        url_path='onlogin',
        permission_classes=[AllowAny],

    )
    def on_login(self, request):
        """
        Action  view to create user
        """

        data = self.request.data

        username = data['username']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        age = data['age']
        gender = data['gender']
        designation = data['designation']
        bio = data['bio']
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            data = 'Passwords dont match'
            return Response(
                data=data,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            try:
                user = User.objects.get(username=username)
                data = 'User with that username already exists'

                return Response(
                    data=data,
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    age=age,
                    gender=gender,
                    designation=designation,
                    bio=bio,
                    password=password
                )
                user.is_superuser = False
                user.is_staff = True
                user.save()
                data = 'User Created'
                login(request=request, user=user)
                return Response(
                    data=data,
                    status=status.HTTP_201_CREATED
                )

    @action(
        methods=['POST', ],
        detail=False,
        url_name='onlogout',
        url_path='onlogout',
        permission_classes=[IsAuthenticated],

    )
    def on_logout(self, request):
        """
        Action view to logout user
        """
        logout(request)
        return Response(
            {
                'message': 'Logged out. Bye!',
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST', ],
        detail=False,
        url_name='verifyuser',
        url_path='verifyuser',
        permission_classes=[AllowAny],

    )
    def verify_user(self, request):
        """
        Action view to login user
        """

        data = self.request.data

        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return Response(
                {
                    'message': f'You are now logged in as {username}',
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'Access Denied',
                },
                status=status.HTTP_400_BAD_REQUEST
            )