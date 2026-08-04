from rest_framework import permissions, viewsets

from .models import Character
from .serializers import CharacterSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    """CRUD des personnages appartenant à l'utilisateur connecté."""

    serializer_class = CharacterSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
