from rest_framework import serializers

from .models import GameModel, GamePlayer, GameBoard, GameRecord

class GamePlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamePlayer
        fields = ('name', 'image', 'color_r', 'color_g', 'color_b',)

class GameBoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameBoard
        fields = ('game', 'size', 'state',)

class GameRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameRecord
        fields = ('game', 'player', 'action', 'pos_x', 'pos_y',)

class GameModelSerializer(serializers.ModelSerializer):
    players = GamePlayerSerializer(many=True)
    board   = GameBoardSerializer()

    class Meta:
        model = GameModel
        fields = ('id', 'title', 'created_date', 'players', 'board', 'active_player_idx', 'is_game_end',)
