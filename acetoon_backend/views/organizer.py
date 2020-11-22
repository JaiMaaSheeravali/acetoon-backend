from acetoon_backend.models import Organizer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from acetoon_backend.serializers import OrganizerSerializer


class CreateOrganizer(viewsets.ModelViewSet):
    """
    Views to create Organizer
    """

    permission_classes = [IsAuthenticated, ]
    http_method_names = ['post', 'get', 'patch']
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
