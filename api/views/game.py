from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models.game import Game
from api.serializers.game_serializer import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def uploaded_images(self, request, pk=None):
        game = Game.objects.filter(pk=pk)
        uploaded_images = game.images.all().count()
        return Response({'uploadedImages': str(uploaded_images)})