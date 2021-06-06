// 即時関数として定義
(function (global) { // globalオブジェクトを取得
  "use strict"; // strictモード
  // Class ------------------------------------------------
  function EventReceipter() {}

  // Header -----------------------------------------------
  global.EventReceipter = EventReceipter;
  global.EventReceipter.init = init;

  // Const ------------------------------------------------
  var BOARD_SIZE;
  var RECT_CANV;
  var CELL_SIZE;

  // Variable ---------------------------------------------
  var canv_ctx;

  // Function ---------------------------------------------
  // 初期化
  function init(_canv_ctx, board_size, rect_board) {
    canv_ctx   = _canv_ctx;
    BOARD_SIZE = board_size;
    RECT_CANV  = rect_board;
    CELL_SIZE  = RECT_CANV.w / BOARD_SIZE | 0;
    setEvents();
  }

  // イベントの関連付け
  function setEvents() {
    var isTouch;
    if (window.ontouchstart === null) {
      isTouch = true;
    } else {
      isTouch = false;
    }
    
    if (isTouch) {
      canv_ctx.canvas.addEventListener('touchstart', ev_mouseClick)
    } else {
      canv_ctx.canvas.addEventListener('mousemove', ev_mouseMove)
      canv_ctx.canvas.addEventListener('mouseup', ev_mouseClick)
      canv_ctx.canvas.addEventListener('touchstart', ev_mouseClick) //スマホが反応しないので無理やり
    }
  }

  // マウスカーソル移動のイベント処理
  function ev_mouseMove(e) {
    const point = getMousePosition(e);
    const selected = hitTest(point);
    // 画面描画
    Render.render(false, selected);
  }

  // マウスクリックのイベント処理
  function ev_mouseClick(e) {
    const point = getMousePosition(e);
    const selected = hitTest(point);

    if (selected.name === "RECT_CANV") {
      // APIにて石設置アクションの実行要求
      const data = {"player_id":1, "action":"action_set_peace",
                    "pos_x":selected.pos.x, "pos_y":selected.pos.y,}
      ApiController.sendApiRequest("PATCH", "try_player_action/", data).then(response => {
        console.log(response);
        // 画面描画
        Render.render(true, selected);
      })
    }
  }

  // マウスカーソルの位置を取得する
  function getMousePosition(e) {
    if (!e.clientX) { //SmartPhone
      if (e.touches) {
        e = e.originalEvent.touches[0];
      } else if (e.originalEvent.touches) {
        e = e.originalEvent.touches[0];
      } else {
        e = event.touches[0];
      }
    }
    var rect = e.target.getBoundingClientRect();
    var point = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
    return point;
  }

  // マウスカーソルの座標を取得する
  function hitTest(point) {
    var objects = [RECT_CANV];
    var click_obj = null;
    var selected = {
      name: "",
      pos: {x:-1, y:-1}
    }
    for (var i = 0; i < objects.length; i++) {
      if (objects[i].w >= point.x && objects[i].x <= point.x && objects[i].h >= point.y && objects[i].y <= point.y) {
        selected.name = "RECT_CANV";
        break;
      }
    }

    switch (true) {
    case selected.name === "RECT_CANV":
      const x = Math.floor(point.x / CELL_SIZE);
      const y = Math.floor(point.y / CELL_SIZE);
      if (0 <= x && x < BOARD_SIZE) {
        selected.pos.x = x;
      }
      if (0 <= y && y < BOARD_SIZE) {
        selected.pos.y = y;
      }
      break;
    }
    return selected;
  }

})((this || 0).self || global);
