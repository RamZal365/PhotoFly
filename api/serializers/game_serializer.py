from rest_framework import serializers

from api.models.game import GameImage, Game


class GameImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameImage
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    images = GameImageSerializer(many=True, required=False)

    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at',)
