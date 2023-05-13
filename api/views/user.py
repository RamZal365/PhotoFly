from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models.user import CustomUser
from api.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def join_game(self, request, pk=None):

        return Response({'message': 'Hello, world!'})