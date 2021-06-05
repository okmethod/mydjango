from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GameModel, GamePlayer, GameBoard, GameRecord
from .serializer import GameModelSerializer, GameRecordSerializer

def home(request):
    games = GameModel.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'reversi/game_list.html', {'games': games})

def game(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    return render(request, 'reversi/game_detail.html', {'game': game})

# ゲームの公開情報をまとめて取得する
class GameModelViewSet(viewsets.ModelViewSet):
    queryset = GameModel.objects.all()
    serializer_class = GameModelSerializer
    filter_fields = ()

# プレイヤーアクションを登録する
class GameRecordViewSet(viewsets.ModelViewSet):
    queryset = GameRecord.objects.all()
    serializer_class = GameRecordSerializer
    filter_fields = ('game',)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # アクション：石を置く
    @action(methods=['post'], detail=False)
    def try_player_action(self, request):
        game   = GameModel.objects.get(id=request.data['game'])
        player = GamePlayer.objects.get(id=request.data['player'])
        number = game.get_num_of_records() + 1
        action = request.data['action']
        pos    = (int(request.data['pos_x']), int(request.data['pos_y']))

        # 盤面の操作
        game.board.set_piece_at_pos(pos, '1')
        game.board.save()

        # 棋譜の追加
        record = GameRecord(
                    game=game,
                    player=player,
                    number=number,
                    action=action,
                    pos_x=pos[0],
                    pos_y=pos[1],)
        record.save()

        result = { 'valid':True, 'number':number, 'action':action, 'pos':pos}

        return Response(status=status.HTTP_201_CREATED, data=result)
