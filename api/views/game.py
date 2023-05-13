from rest_framework import viewsets, permissions

from api.models.game import Game
from api.serializers.game_serializer import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]
