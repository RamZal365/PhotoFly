from rest_framework import serializers
from api.models.user import CustomUser
from api.serializers.game_serializer import GameSerializer


class UserSerializer(serializers.ModelSerializer):
    game = GameSerializer(allow_null=True)
    score = serializers.IntegerField(allow_null=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ('created_at',)
