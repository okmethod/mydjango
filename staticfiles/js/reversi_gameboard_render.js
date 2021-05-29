// 即時関数として定義
(function (global) { // globalオブジェクトを取得
    "use strict"; // strictモード
    // Class ------------------------------------------------
    function Render() {}

    // Header -----------------------------------------------
    global.Render = Render;
    global.Render.render = render;
    global.Render.RECT_BOARD = RECT_BOARD;
    global.Render.CELL_SIZE = CELL_SIZE;

    // Const ------------------------------------------------
    var COL = 8;
    var RECT_CANV = {
        x: 0, y: 0, w: 500, h: 500
    };
    var RECT_BOARD = {
        x: 0, y: 0, w: 500, h: 500
    };
    var CELL_SIZE = RECT_CANV.w / COL | 0;

    var COLOR_BOARD  = "#00A000";
    var COLOR_LINE   = "#006400";
    var COLOR_WHITE  = "#FFFFFF";
    var COLOR_BLACK  = "#000000";
    var COLOR_SELECT = "#FFFFFF";

    // Variable ---------------------------------------------
    var state_cache = null;
    var prev_revision = -1;
    var canv_cache = {      // ゲーム画面全体のキャッシュ
        canv_board: null,   // 盤
        canv_pieaces: null, // 石
        canv_effect: null   // エフェクト
    };

    // Function ---------------------------------------------
    // ゲーム画面全体を描画する
    function render(ctx, state, point) {
        // 描画対象物を生成してキャッシュに保持
        if (prev_revision < 0) { // 初期状態の場合、すべて描画
            canv_cache.canv_board = drawBoard(state);
            canv_cache.canv_pieaces = drawPieceALL(state);
            canv_cache.canv_effect = drawEffect(state);
            Render.RECT_BOARD = RECT_BOARD;
            Render.CELL_SIZE = CELL_SIZE;
        } else { // 初期状態でない場合、必要箇所のみ描画
            if (state.revision != prev_revision) { // 盤面が変化している場合のみ
                canv_cache.canv_pieaces = drawPieceALL(state);
            }
            canv_cache.canv_effect = drawEffect(state, point);
        }

        // キャッシュから描画
        ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);
        ctx.drawImage(canv_cache.canv_board, 0, 0, RECT_CANV.w, RECT_CANV.h);
        ctx.drawImage(canv_cache.canv_pieaces, 0, 0, RECT_CANV.w, RECT_CANV.h);
        ctx.drawImage(canv_cache.canv_effect, 0, 0, RECT_CANV.w, RECT_CANV.h);
        prev_revision = state.revision;
    }

    // 盤を描画する
    function drawBoard(state) {
        // 盤のキャッシュの原型を生成
        if (!canv_cache.canv_board) {
            canv_cache.canv_board = document.createElement("canvas");
            canv_cache.canv_board.width = RECT_CANV.w;
            canv_cache.canv_board.height = RECT_CANV.h;
        }

        // 2Dグラフィックスのコンテキストオブジェクトを取得
        var ctx = canv_cache.canv_board.getContext('2d');
        ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);

        // 背景色
        ctx.fillStyle = COLOR_BOARD;

        // 罫線
        for (var x = 0; x < COL; x++) {
            for (var y = 0; y < COL; y++) {
                ctx.strokeStyle = COLOR_LINE;
                ctx.beginPath();
                ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
                ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }

        // 盤キャッシュを返却
        return canv_cache.canv_board;
    }

    // 石をすべて描画する
    function drawPieceALL(state) {
        // 石キャッシュの原型を生成
        if (!canv_cache.canv_pieaces) {
            canv_cache.canv_pieaces = document.createElement("canvas");
            canv_cache.canv_pieaces.width = RECT_CANV.w;
            canv_cache.canv_pieaces.height = RECT_CANV.h;
        }

        // 2Dグラフィックスのコンテキストオブジェクトを取得
        var ctx = canv_cache.canv_pieaces.getContext('2d');
        ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);

        // すべてのマスをループ
        for (var x = 0; x < COL; x++) {
            for (var y = 0; y < COL; y++) {
                if (state.map[y * COL + x] != 0) {
                    // 石を1つを描画
                    drawPiece(ctx, x * CELL_SIZE, y * CELL_SIZE, state.map[y * COL + x]);
                }
            }
        }

        // 石キャッシュを返却
        return canv_cache.canv_pieaces;
    }

    // 石を1つ描画する
    function drawPiece(ctx, x, y, number) {

        // 石色の設定
        if (number > 0) { // 白石の設定
            ctx.fillStyle = COLOR_WHITE;
        } else if (number < 0) { // 黒石の設定
            ctx.fillStyle = COLOR_BLACK;
        }

        // 影の設定
        ctx.shadowBlur = 20;
        ctx.shadowColor = "rgba(0, 0, 0, 1)";
        ctx.shadowOffsetX = 5;
        ctx.shadowOffsetY = 5;

        // 石の描画
        ctx.beginPath();
        ctx.arc(x + CELL_SIZE/2, y + CELL_SIZE/2, (CELL_SIZE*0.9)/2, 0, Math.PI*2, false);
        ctx.fill();

        // 石コンテキストを返却
        return ctx;
    }

    // エフェクトを描画する
    function drawEffect(state) {

        // エフェクトキャッシュの原型を生成
        if (!canv_cache.canv_effect) {
            canv_cache.canv_effect = document.createElement("canvas");
            canv_cache.canv_effect.width = RECT_CANV.w;
            canv_cache.canv_effect.height = RECT_CANV.h;
        }

        // 2Dグラフィックスのコンテキストオブジェクトを取得
        var ctx = canv_cache.canv_effect.getContext('2d');
        ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);

        // カーソル位置を取得
        var x = (state.selected.value % COL | 0);
        var y = (state.selected.value / COL | 0);

        // カーソル
        ctx.fillStyle = COLOR_SELECT;
        ctx.globalAlpha = 0.5;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

        // エフェクトキャッシュを返却
        return canv_cache.canv_effect;
    }

})((this || 0).self || global);
