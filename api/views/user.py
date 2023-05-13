from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models.game import Game
from api.models.user import CustomUser
from api.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def join_game(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)

        if "code" in request.data:
            code = request.data['code'];
            games_qs = Game.objects.filter(code=code)

            if games_qs.exists():   # El objeto existe, puedes acceder a él
                gameObject = games_qs.first()
                if(gameObject)

            else:             # El objeto no existe
                return Response({'errorCode': 1 ,'message': 'Sala no encontrada'})
            pass

        else:

            pass
        return Response({'message': 'Hello, world!'})