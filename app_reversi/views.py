from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import GameModel, GamePlayer, GameBoard, GameRecord
from .serializer import GamePlayerSerializer, GameBoardSerializer

def home(request):
    games = GameModel.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'reversi/game_list.html', {'games': games})

def game(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    return render(request, 'reversi/game_detail.html', {'game': game})

class GamePlayerViewSet(viewsets.ModelViewSet):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerSerializer
    filter_fields = ('game',)

class GameBoardViewSet(viewsets.ModelViewSet):
    queryset = GameBoard.objects.all()
    serializer_class = GameBoardSerializer
    filter_fields = ('game',)
