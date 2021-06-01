from rest_framework import serializers

from .models import GamePlayer, GameBoard

class GamePlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamePlayer
        fields = ('game', 'name', 'image', 'color_r', 'color_g', 'color_b',)

class GameBoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameBoard
        fields = ('game', 'size', 'state',)
