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

def game_room(request, pk):
    game = get_object_or_404(GameModel, pk=pk)
    return render(request, 'reversi/game_detail.html', {'game': game})

# ゲーム全体
class GameModelViewSet(viewsets.ModelViewSet):
    queryset = GameModel.objects.all()
    serializer_class = GameModelSerializer
    filter_fields = ()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 新しいゲームを開始する
    @action(methods=['PATCH'], detail=True)
    def restart_game(self, request, pk):
        game = GameModel.objects.get(id=pk)

        result = game.restart_game()
        game.save()
        game.board.save()

        return Response(status=status.HTTP_200_OK, data=result)

    # プレイヤーアクションを受け付ける
    @action(methods=['PATCH'], detail=True)
    def try_player_action(self, request, pk):
        game = GameModel.objects.get(id=pk)
        player = GamePlayer.objects.get(id=request.data['player_id'])
        action = request.data['action']

        if 'pos_x' in request.data.keys():
            pos_x = int(request.data['pos_x'])
        else:
            pos_x = None
        if 'pos_y' in request.data.keys():
            pos_y = int(request.data['pos_y'])
        else:
            pos_y = None
        pos = (pos_x, pos_y)

        # その場しのぎコード　※本来は要求プレイヤーのidxを算出
        player_idx = game.active_player_idx

        # アクションを施行
        if action == "action_set_peace":
            result = game.action_set_peace(player_idx, pos)
            result['action'] = action
            result['pos']    = pos
        elif action == "action_pass":
            result = game.action_pass(player_idx)
            result['action'] = action
        else:
            description_str = 'invalid action'
            result = {'is_valid' : False, 'description' : description_str}

        # アクションが有効だった場合
        if result['is_valid']==True:
            number = game.get_num_of_records() + 1
            game.board.save()
            game.save()

            # 棋譜の追加
            record = GameRecord(
                        game=game,
                        player=player,
                        number=number,
                        action=action,
                        pos_x=pos_x,
                        pos_y=pos_y,)
            record.save()

            return Response(status=status.HTTP_200_OK, data=result)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data=result)
