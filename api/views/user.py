from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from api.choices import STATE, MAX_USERS, ROOM_FOUND_CODE, ROOM_BUSY_CODE, \
    ROOM_NOT_FOUND_CODE, JOIN_STARTING_ROOM_CODE, JOIN_WAITING_ROOM_CODE, DEPARTURE_CITY, \
    ARRIVAL_CITY, ROOM_CREATED, WAITING, NOT_AN_ADMIN, NOT_IN_A_GAME, GAME_HAS_ALREADY_STARTED, NEED_MORE_PLAYERS, \
    UPLOAD_IMAGES, UPLOADING_IMAGES, NEED_MORE_IMAGES

from api.models.game import Game
from api.models.user import CustomUser
from api.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['post'])
    def join_game(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)
        games = Game.objects.all()

        if "code" in request.data:
            code = request.data['code']
            games_qs = games.filter(code=code)

            if games_qs.exists():  # El objeto existe, puedes acceder a él
                game_object = games_qs.first()

                if game_object.state == WAITING:
                    return UserViewSet.add_user_to_room(game_object, user)

                else:
                    return Response({'responseCode': ROOM_BUSY_CODE, 'message': 'No es posible acceder, partida iniciada'})

            else:  # El objeto no existe
                return Response({'responseCode': ROOM_NOT_FOUND_CODE, 'message': 'Sala no encontrada'})
            pass

        elif games.filter(state=WAITING).exists():
            return UserViewSet.add_user_to_room(games.filter(state=WAITING).first(), user)

        else:
            game = Game(
                code=00000,
                round=1,
                state=WAITING,
                departure_city=DEPARTURE_CITY,
                arrival_city=ARRIVAL_CITY)

            game.code = game.generate_room_code()
            user.game = game
            game.save()
            user.is_admin = True
            user.save()

            return Response({'responseCode': ROOM_CREATED, 'message': 'Sala creada'})

    @staticmethod
    def add_user_to_room(game_object, user):
        user.game = game_object
        user.save()
        game_u_count = game_object.users.all().count()
        if game_u_count == MAX_USERS:
            game_object.upload_images()
            return Response(
                {'responseCode': JOIN_WAITING_ROOM_CODE, 'message': 'Accediendo a sala espera'})

        else:
            return Response({'gameId': str(game_object.id), 'responseCode': JOIN_WAITING_ROOM_CODE, 'message': 'Accediendo a sala espera'})

    @action(detail=True, methods=['post'])
    def upload_images(self, request, pk=None):
        user = CustomUser.objects.filter(pk=pk)
        if not user.is_admin:
            return Response({'responseCode': NOT_AN_ADMIN, 'message': 'You are not an admin'})

        game = user.game
        if not game:
            return Response({'responseCode': NOT_IN_A_GAME, 'message': 'You are not in a game'})

        if game.state != WAITING:
            return Response({'responseCode': GAME_HAS_ALREADY_STARTED, 'message': 'The game has already started'})

        if game.users.all().count() == 1:
            return Response({'responseCode': NEED_MORE_PLAYERS, 'message': "You can't start a game with less then 2 players"})
        game.upload_images()
        return Response({'responseCode': UPLOAD_IMAGES, 'message': "Upload images"})

    @action(detail=True, methods=['post'])
    def start_game(self, request, pk=None):
        user = CustomUser.objects.filter(pk=pk)
        if not user.is_admin:
            return Response({'responseCode': NOT_AN_ADMIN, 'message': 'You are not an admin'})

        game = user.game
        if not game:
            return Response({'responseCode': NOT_IN_A_GAME, 'message': 'You are not in a game'})

        if game.state != UPLOADING_IMAGES:
            return Response({'responseCode': GAME_HAS_ALREADY_STARTED, 'message': 'The game has already started'})

        if game.users.all().count() == 1:
            return Response(
                {'responseCode': NEED_MORE_PLAYERS, 'message': "You can't start a game with less then 2 players"})

        if game.images.all().count() < 10:
            return Response(
                {'responseCode': NEED_MORE_IMAGES, 'message': "You can't start a game with less then 10 images"})

        game.start_game()
        return Response({'responseCode': UPLOAD_IMAGES, 'message': "Upload images"})