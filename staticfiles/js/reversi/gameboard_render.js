// 即時関数として定義
(function (global) { // globalオブジェクトを取得
  "use strict"; // strictモード
  // Class ------------------------------------------------
  function Render() {}

  // Header -----------------------------------------------
  global.Render = Render;
  global.Render.init   = init;
  global.Render.render = render;

  // Const ------------------------------------------------
  var BOARD_SIZE;
  var RECT_CANV;
  var CELL_SIZE;

  var COLOR_PLAYER1  = "#000000";
  var COLOR_PLAYER2  = "#FFFFFF";
  const COLOR_BOARD  = "#00A000";
  const COLOR_LINE   = "#006400";
  const COLOR_SELECT = "#FFFFFF";

  // Variable ---------------------------------------------
  var canv_ctx;
  var state;

  var canv_cache = {      // ゲーム画面全体のキャッシュ
    canv_board: null,   // ボード
    canv_pieaces: null, // 石
    canv_highlight: null   // 指定マスのハイライト
  };

  // Function ---------------------------------------------
  // 初期化
  function init(_canv_ctx, board_size, rect_board, p1_color, p2_color) {
    canv_ctx   = _canv_ctx;
    BOARD_SIZE = board_size;
    RECT_CANV  = rect_board;
    CELL_SIZE  = RECT_CANV.w / BOARD_SIZE | 0;
    COLOR_PLAYER1 = rgb2hex(p1_color);
    COLOR_PLAYER2 = rgb2hex(p2_color);

    // ボードキャッシュの原型を作成
    canv_cache.canv_board = document.createElement("canvas");
    canv_cache.canv_board.width  = RECT_CANV.w;
    canv_cache.canv_board.height = RECT_CANV.h;
    // ボードキャッシュは初めに1回だけ作成する
    canv_cache.canv_board = updateCacheBoard()

    // 石キャッシュの原型を生成
    canv_cache.canv_pieaces = document.createElement("canvas");
    canv_cache.canv_pieaces.width = RECT_CANV.w;
    canv_cache.canv_pieaces.height = RECT_CANV.h;

    // ハイライトキャッシュの原型を生成
    canv_cache.canv_highlight = document.createElement("canvas");
    canv_cache.canv_highlight.width = RECT_CANV.w;
    canv_cache.canv_highlight.height = RECT_CANV.h;

    // 画面描画
    render(true);
  }

  // 画面更新
  function render(please_api_get, selected=null) {
    // セル位置が指定されている場合
    if (selected != null) {
      // ハイライトキャッシュを更新
      canv_cache.canv_highlight = updateCacheHighlight(selected);
    }
    // 情報取得を求められている場合
    if (please_api_get) {
      // APIにてゲームの公開情報を取得
      ApiController.sendApiRequest("GET", "").then(response => {
        console.log(response);
        state    = response.board.state;
        // 石キャッシュを更新
        canv_cache.canv_pieaces = updateCachePieces(state);
        // 画面描画
        drawAll(selected);
      })
    } else {
      // 画面描画
      drawAll(selected);
    }
  }

  // ゲーム画面全体を描画する
  function drawAll() {
    // キャッシュから描画
    canv_ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);
    canv_ctx.drawImage(canv_cache.canv_board,     0, 0, RECT_CANV.w, RECT_CANV.h);
    canv_ctx.drawImage(canv_cache.canv_pieaces,   0, 0, RECT_CANV.w, RECT_CANV.h);
    canv_ctx.drawImage(canv_cache.canv_highlight, 0, 0, RECT_CANV.w, RECT_CANV.h);
  }

  // ボードキャッシュを更新する
  function updateCacheBoard() {

    // 2Dグラフィックスのコンテキストオブジェクトを取得
    var ctx = canv_cache.canv_board.getContext('2d');
    ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);

    // 背景色
    ctx.fillStyle = COLOR_BOARD;

    // 罫線
    for (var x = 0; x < BOARD_SIZE; x++) {
      for (var y = 0; y < BOARD_SIZE; y++) {
        ctx.strokeStyle = COLOR_LINE;
        ctx.beginPath();
        ctx.fillRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
        ctx.strokeRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
      }
    }

    // ボードキャッシュを返却
    return canv_cache.canv_board;
  }

  // 石キャッシュを更新する
  function updateCachePieces(state=null) {

    // 2Dグラフィックスのコンテキストオブジェクトを取得
    var ctx = canv_cache.canv_pieaces.getContext('2d');
    ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);

    // すべてのマスをループ
    var cell_state;
    for (var x = 0; x < BOARD_SIZE; x++) {
      for (var y = 0; y < BOARD_SIZE; y++) {
        cell_state = state.substr(y*BOARD_SIZE + x, 1);
        if (cell_state  != "0") {
          // 石1つを追加
          addPiece(ctx, x*CELL_SIZE, y*CELL_SIZE, cell_state);
        }
      }
    }

    // 石キャッシュを返却
    return canv_cache.canv_pieaces;
  }

  // 石を1つ描画する
  function addPiece(ctx, x, y, player_idx) {

    // 石色の設定
    if (player_idx == "1") { // 黒石の設定
      ctx.fillStyle = COLOR_PLAYER1;
    } else if (player_idx == "2") { // 白石の設定
      ctx.fillStyle = COLOR_PLAYER2;
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

  // ハイライトキャッシュを更新する
  function updateCacheHighlight(selected=null) {

    // ボード内が指定されている場合のみ
    if (selected.name = "RECT_CANV") {
      // 2Dグラフィックスのコンテキストオブジェクトを取得
      var ctx = canv_cache.canv_highlight.getContext('2d');
      ctx.clearRect(0, 0, RECT_CANV.w, RECT_CANV.h);

      // 指定マスにハイライトを追加
      ctx.fillStyle = COLOR_SELECT;
      ctx.globalAlpha = 0.5;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.fillRect(selected.pos.x * CELL_SIZE, selected.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE);
    }

    // ハイライトキャッシュを返却
    return canv_cache.canv_highlight;
  }

  // RGBをHEXに変換する
  function rgb2hex(rgb) {
    return "#" + rgb.map( function ( value ) {
      return ( "0" + value.toString( 16 ) ).slice( -2 ) ;
    } ).join( "" ) ;
  }

})((this || 0).self || global);
