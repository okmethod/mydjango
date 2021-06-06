from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Const
BOARD_SIZE = 8
BLANK_IDX   = 0
PLAYER1_IDX = 1
PLAYER2_IDX = 2

# ゲーム全体の管理
class GameModel(models.Model):
    title         = models.CharField(max_length=64)
    created_date  = models.DateTimeField(default=timezone.now)
    active_player_idx = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])
    winner_player_idx = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)])
    is_game_end   = models.BooleanField(default=False)

    # レコード名
    def __str__(self):
        return self.title

    # getter : アクション履歴の数を取得する
    def get_num_of_records(self):
        return self.records.count()

    # getter : 指定プレイヤーを取得する
    def get_player(self, player_idx):
        if player_idx == 1:
            return self.players.first()
        elif player_idx == 2:
            return self.players.last()

    # getter : プレイヤー1を取得する
    def get_player1(self):
        return self.get_player(1)

    # getter : プレイヤー2を取得する
    def get_player2(self):
        return self.get_player(2)

    # getter : アクティブプレイヤーを取得する
    def get_active_player(self):
        return get_player(self.active_player_idx)

    # getter : 次のプレイヤーを取得する
    def get_next_player(self):
        if self.active_player_idx == 1:
            return get_player(2)
        elif self.active_player_idx == 2:
            return get_player(1)

    # getter : 指定プレイヤーの得点を取得する
    def get_players_points(self, player_idx):
        return self.board.get_num_of_piece(player_idx)

    # 内部メソッド : 得点が多いプレイヤーを勝利プレイヤーととし、ゲームを終了する
    def judge_dominant(self):
        if get_players_points(1) > get_players_points(2):
            winner_player_idx = 1
        elif get_players_points(1) < get_players_points(2):
            winner_player_idx = 2
        else:
            winner_player_idx = 0
        self.is_game_end = True

    # 内部メソッド : アクティブプレイヤーを交代する
    def change_turn(self):
        if self.active_player_idx == 1:
            self.active_player_idx = 2
        elif self.active_player_idx == 2:
            self.active_player_idx = 1

    # 内部メソッド : ゲームを初期化する
    def restart_game(self):

        # 管理情報の初期化
        self.active_player_idx = 1
        self.winner_player_idx = 0
        self.is_game_end = False
        # ボードの初期化
        self.board.init_state()
        # アクション履歴の削除
        self.records.all().delete()

        description_str = 'New game is starting.'
        return {'is_valid' : True, 'description' : description_str}

    # プレイヤーアクション：石を設置する
    def action_set_peace(self, player_idx, pos):
        pos_x, pos_y = pos[0], pos[1]

        # ゲーム終了フラグがONの場合、何もしない
        if self.is_game_end:
            # アクションの結果を返却する
            description_str = 'This game has terminated.'
            return {'is_valid' : False, 'description' : description_str}

        # 要求プレイヤーがアクティブでない場合、何もしない
        if player_idx != self.active_player_idx:
            # アクションの結果を返却する
            description_str = 'This turn is NOT yours.'
            return {'is_valid' : False, 'description' : description_str}

        # 指定位置が有効手かどうかを確認する
        action_result = self.board.validate_set_pos(player_idx, pos)

        # 有効手であった場合
        if action_result['is_valid']:
            # 当該マスをターンプレイヤーの色に変更する
            self.board.set_piece_at_pos(player_idx, pos)
            # 石を反転する(8方向)
            self.board.reverse_peaces(player_idx, pos, [ 0, -1], True) # 上
            self.board.reverse_peaces(player_idx, pos, [ 1, -1], True) # 右上
            self.board.reverse_peaces(player_idx, pos, [ 1,  0], True) # 右
            self.board.reverse_peaces(player_idx, pos, [ 1,  1], True) # 右下
            self.board.reverse_peaces(player_idx, pos, [ 0,  1], True) # 下
            self.board.reverse_peaces(player_idx, pos, [-1,  1], True) # 左下
            self.board.reverse_peaces(player_idx, pos, [-1,  0], True) # 左
            self.board.reverse_peaces(player_idx, pos, [-1, -1], True) # 左上
            # 空マスが残っていなければ、勝者を判定してゲーム終了フラグをオンにする
            if self.board.get_num_of_piece(BLANK_IDX) == 0:
                self.judge_dominant()
            # ターンプレイヤーを交代する
            self.change_turn()
            # アクションの結果を返却する
            description_str = 'The specified position flipped some peaces.'
            return {'is_valid' : True, 'description' : description_str}
        else:
            # アクションの結果を返却する
            return {'is_valid' : False, 'description' : action_result['description']}

    # プレイヤーアクション : パスする
    def action_pass(self, player_idx):

        # ゲーム終了フラグがONの場合、何もしない
        if self.is_game_end:
            # アクションの結果を返却する
            description_str = 'This game has terminated.'
            return {'is_valid' : False, 'description' : description_str}

        # 要求プレイヤーがアクティブでない場合、何もしない
        if player_idx != self.active_player_idx:
            # アクションの結果を返却する
            description_str = 'This turn is NOT yours.'
            return {'is_valid' : False, 'description' : description_str}

        # 各マスを確認し、有効手が残っていれば何もしない
        for pos_x in range(self.board.size):
            for pos_y in range(self.board.size):
                if self.board.validate_set_pos(player_idx, (pos_x, pos_y))['is_valid']:
                    # アクションの結果を返却する
                    description_str = 'Some valid position are left.'
                    return {'is_valid' : False, 'description' : description_str}

        # パスが連続している場合
        if self.records.last().action == 'pass':
            # 勝者を判定してゲーム終了フラグをオンにする
            self.judge_dominant()
            description_str = 'No valid position are left for any players.'
        else:
            # パスフラグをオンにし、ターンプレイヤーを交代する
            self.change_turn()
            description_str = 'Active player is changed.'

        # アクションの結果を返却する
        return {'is_valid' : True, 'description' : description_str}


    # プレイヤーアクション : 投了する
    def action_give_up(self, player_idx):

        # ゲーム終了フラグがONの場合、何もしない
        if self.is_game_end:
            # アクションの結果を返却する
            description_str = 'This game has terminated.'
            return {'is_valid' : False, 'description' : description_str}

        # 非アクティブプレイヤーを勝者とし、ゲーム終了フラグをオンにする
        if player_idx == 1:
            self.winner_player_idx = 2
        elif player_idx == 2:
            self.winner_player_idx = 1
        self.is_game_end = True

        # アクションの結果を返却する
        description_str = 'Active player gave up.'
        return {'is_valid' : True, 'description' : description_str}

# プレイヤー情報
class GamePlayer(models.Model):
    # リレーション
    game = models.ForeignKey('app_reversi.GameModel', on_delete=models.CASCADE, related_name='players')
    # フィールド
    name       = models.CharField(max_length=20)
    color_r    = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    color_g    = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    color_b    = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    image      = models.ImageField(null=True, blank=True)
    use_image  = models.BooleanField(default=False)
    #is_active  = models.BooleanField(default=False)
    #is_winner  = models.BooleanField(default=False)
    #is_passing = models.BooleanField(default=False)

    # レコード名
    def __str__(self):
        return self.name


# ボード状況
class GameBoard(models.Model):
    # リレーション
    game = models.OneToOneField('app_reversi.GameModel', on_delete=models.CASCADE, related_name='board')
    # フィールド
    size  = models.PositiveSmallIntegerField(default=BOARD_SIZE)
    state = models.CharField(default=str(BLANK_IDX)*(BOARD_SIZE**2), max_length=(BOARD_SIZE**2))

    # レコード名
    def __str__(self):
        return self.state

    # init : 盤面の初期化
    def init_state(self):
        self.state = str(BLANK_IDX)*(self.size**2)
        self.set_piece_at_pos(str(PLAYER2_IDX), (self.size//2,  self.size//2  ))
        self.set_piece_at_pos(str(PLAYER1_IDX), (self.size//2,  self.size//2-1))
        self.set_piece_at_pos(str(PLAYER1_IDX), (self.size//2-1,self.size//2  ))
        self.set_piece_at_pos(str(PLAYER2_IDX), (self.size//2-1,self.size//2-1))

    # getter : 指定座標の石を取得する
    def get_piece_at_pos(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        return self.state[pos_y*self.size + pos_x]

    # setter : 指定座標の石を更新する
    def set_piece_at_pos(self, player_idx, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        pos_idx = pos_y*self.size + pos_x
        state_str = self.state
        self.state = state_str[:pos_idx] + str(player_idx) + state_str[pos_idx+1:]

    # getter : 指定色の石数を取得する
    def get_num_of_piece(self, player_idx):
        return self.state.count(str(player_idx))

    # 指定した方向の石を反転する(またはシミュレーションする)
    def reverse_peaces(self, player_idx, pos, dir, update_flg):
        pos_x, pos_y  = pos[0], pos[1]
        dir_x, dir_y  = dir[0], dir[1]

        # 反転位置を保持する配列
        reverse_pos_list = []

        # はみ出さない限り、繰り返す
        while (pos_x + dir_x >= 0) and (pos_x + dir_x <= self.size-1) and \
              (pos_y + dir_y >= 0) and (pos_y + dir_y <= self.size-1):

            # 指定された方向の隣の位置の石を取得
            pos_x = pos_x + dir_x
            pos_y = pos_y + dir_y
            pos = (pos_x, pos_y)
            piece_state = self.get_piece_at_pos(pos)

            # 空白の場合
            if piece_state == str(BLANK_IDX):
                break
            # 同じ色でない場合
            elif piece_state != str(player_idx):
                # 反転位置を予約する
                reverse_pos_list.append(pos)
            # 同じ色の場合
            elif piece_state == str(player_idx):
                # 1つ以上の反転位置が予約されている場合
                if len(reverse_pos_list) > 0:
                    # 更新フラグがONの場合、予約位置を更新する
                    if update_flg:
                        for reverse_pos in reverse_pos_list:
                            self.set_piece_at_pos(player_idx, reverse_pos)
                    # 反転する石があったので、Trueを返す
                    return True
        # 反転する石がなかったので、Falseを返す
        return False

    # 指定位置が有効手かどうかを判定する
    def validate_set_pos(self, player_idx, pos):
        pos_x, pos_y = pos[0], pos[1]

        # 指定位置がボード内の座標かどうかを確認する
        if (pos_y < 0) and (self.size <= pos_y) and \
           (pos_x < 0) and (self.size <= pos_x):
            # 判定結果を返却する
            description_str = 'The specified position is out of range.'
            return {'is_valid' : False, 'description' : description_str}

        # 指定位置が空マスかどうかを確認する
        if self.get_piece_at_pos(pos) != str(BLANK_IDX):
            # 判定結果を返却する
            description_str = 'The specified position is not empty.'
            return {'is_valid' : False, 'description' : description_str}

        # 8方向に対して、石が反転するかどうかを確認する
        if self.reverse_peaces(player_idx, pos, [ 0, -1], False) or \
           self.reverse_peaces(player_idx, pos, [ 1, -1], False) or \
           self.reverse_peaces(player_idx, pos, [ 1,  0], False) or \
           self.reverse_peaces(player_idx, pos, [ 1,  1], False) or \
           self.reverse_peaces(player_idx, pos, [ 0,  1], False) or \
           self.reverse_peaces(player_idx, pos, [-1,  1], False) or \
           self.reverse_peaces(player_idx, pos, [-1,  0], False) or \
           self.reverse_peaces(player_idx, pos, [-1, -1], False):
            # 判定結果を返却する
            description_str = 'The specified position flips some peacess.'
            return {'is_valid' : True, 'description' : description_str}
        else:
            # 判定結果を返却する
            description_str = 'The specified position flips no peacess.'
            return {'is_valid' : False, 'description' : description_str}


# アクション履歴(棋譜)
class GameRecord(models.Model):
    # リレーション
    game   = models.ForeignKey('app_reversi.GameModel', on_delete=models.CASCADE, related_name='records')
    player = models.ForeignKey('app_reversi.GamePlayer', on_delete=models.CASCADE, related_name='records')
    # フィールド
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    action = models.CharField(max_length=64)
    pos_x  = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE)])
    pos_y  = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE)])

    # レコード名
    def __str__(self):
        return "{}: {}_{}".format(self.pk, str(self.number), self.action)

    #
