from django.contrib import admin
from .models import GameModel, GamePlayer, GameBoard, GameRecord

admin.site.register(GameModel)
admin.site.register(GamePlayer)
admin.site.register(GameBoard)
admin.site.register(GameRecord)
