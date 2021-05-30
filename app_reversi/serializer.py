from rest_framework import serializers

from .models import GamePlayer

class GamePlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = GamePlayer
        fields = ('name', 'image', 'color_r', 'color_g', 'color_b',)
