from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from api.choices import STATE, MAX_USERS, ROOM_FOUND_CODE, ROOM_BUSY_CODE, \
    ROOM_NOT_FOUND_CODE, JOIN_STARTING_ROOM_CODE, JOIN_WAITING_ROOM_CODE, DEPARTURE_CITY, \
    ARRIVAL_CITY, ROOM_CREATED, WAITING

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
        games = Game.objects.all()

        if "code" in request.data:
            code = request.data['code']
            games_qs = games.filter(code=code)

            if games_qs.exists():  # El objeto existe, puedes acceder a él
                game_object = games_qs.first()

                if game_object.state == WAITING:
                    return self.add_user_to_room(game_object, user)

                else:
                    return Response({'responseCode': ROOM_BUSY_CODE, 'message': 'No es posible acceder, partida iniciada'})

            else:  # El objeto no existe
                return Response({'responseCode': ROOM_NOT_FOUND_CODE, 'message': 'Sala no encontrada'})
            pass

        elif games.filter(state=WAITING).exists():
            return self.add_user_to_room(games.filter(state=WAITING).first(), user)

        else:
            game = Game(
                 code=00000,
                 round=1,
                 state=WAITING,
                 departure_city=DEPARTURE_CITY,
                 arrival_city=ARRIVAL_CITY)

            game.code = game.generate_room_code()
            user.game = game
            user.is_admin = True
            user.save()
            game.save()

            return Response({'responseCode': ROOM_CREATED, 'message': 'Sala creada'})


    def add_user_to_room(self, game_object, user):
        user.game = game_object
        user.save()
        game_u_count = game_object.users.all().count()
        if game_u_count == MAX_USERS:
            game_object.start_game()
            return Response(
                {'responseCode': JOIN_STARTING_ROOM_CODE, 'message': 'No es posible acceder, partida iniciada'})

        else:
            return Response({'responseCode': JOIN_WAITING_ROOM_CODE, 'message': 'Accediendo a sala espera'})
