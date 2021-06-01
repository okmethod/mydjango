from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Const
BOARD_SIZE = 8

# ゲーム全体の管理
class GameModel(models.Model):
    title        = models.CharField(max_length=64)
    created_date = models.DateTimeField(default=timezone.now)
    is_game_end  = models.BooleanField(default=False)

    # レコード名
    def __str__(self):
        return self.title

    # getter : プレイヤー1を取得する
    def get_player1(self):
        return self.players.first()

    # getter : プレイヤー2を取得する
    def get_player2(self):
        return self.players.last()

    # getter : アクティブプレイヤーを取得する
    def get_active_player(self):
        return self.players.filter(is_active=True)

    # getter : 次のプレイヤーを取得する
    def get_next_player(self):
        return self.players.filter(is_active=False)

    # getter : 勝利プレイヤーを取得する
    def get_winner_player(self):
        return self.players.filter(is_winner=True)


# プレイヤー情報
class GamePlayer(models.Model):
    # リレーション
    game = models.ForeignKey('app_reversi.GameModel', on_delete=models.CASCADE, related_name='players')
    # フィールド
    name       = models.CharField(max_length=20)
    image      = models.ImageField(null=True, blank=True)
    color_r    = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    color_g    = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    color_b    = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(255)])
    is_active  = models.BooleanField(default=False)
    is_winner  = models.BooleanField(default=False)
    is_passing = models.BooleanField(default=False)

    # レコード名
    def __str__(self):
        return self.name


# 盤面情報
class GameBoard(models.Model):
    # 固定値
    DEF_BLANK  = 0
    DEF_COLOR1 = 1
    DEF_COLOR2 = 2
    # リレーション
    game = models.OneToOneField('app_reversi.GameModel', on_delete=models.CASCADE, related_name='board')
    # フィールド
    size  = models.PositiveSmallIntegerField(default=BOARD_SIZE)
    state = models.CharField(default=DEF_BLANK*(BOARD_SIZE*BOARD_SIZE), max_length=(BOARD_SIZE*BOARD_SIZE))

    # レコード名
    def __str__(self):
        return self.state

    # init : 盤面の初期化
    def init_board_state(self):
        self.state = DEF_BLANK*(BOARD_SIZE*BOARD_SIZE)
        self.set_piece_at_pos(self, (self.size//2,  self.size//2  ), DEF_COLOR2)
        self.set_piece_at_pos(self, (self.size//2,  self.size//2-1), DEF_COLOR1)
        self.set_piece_at_pos(self, (self.size//2-1,self.size//2  ), DEF_COLOR1)
        self.set_piece_at_pos(self, (self.size//2-1,self.size//2-1), DEF_COLOR2)

    # getter : 指定座標の石を取得する
    def get_piece_at_pos(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        return self.state[pos_y*self.size + pos_x]

    # setter : 指定座標の石を更新する
    def set_piece_at_pos(self, pos, color):
        pos_x = pos[0]
        pos_y = pos[1]
        if (color==DEF_COLOR1)or(color==DEF_COLOR2):
            self.state[pos_y*self.size + pos_x] = color

    # getter : 指定色の石数を取得する
    def get_num_of_piece(self, color):
        if (color==DEF_BLANK)or(color==DEF_COLOR1)or(color==DEF_COLOR2):
            return self.state.count(color)


# 棋譜情報
class GameRecord(models.Model):
    # リレーション
    game   = models.ForeignKey('app_reversi.GameModel', on_delete=models.CASCADE, related_name='records')
    player = models.OneToOneField('app_reversi.GamePlayer', on_delete=models.CASCADE, related_name='records')
    # フィールド
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    action = models.CharField(max_length=64)
    pos_x  = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE)])
    pos_y  = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE)])

    # レコード名
    def __str__(self):
        return self.state
