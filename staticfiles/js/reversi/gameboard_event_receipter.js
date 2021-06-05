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
    var ctx;
    var state = {}
    var point = {
        x: -1,
        y: -1
    }
    var init_state = {
      map: ["0", "0", "0", "0", "0", "0", "0", "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
            "0", "0", "0", "1", "2", "0", "0", "0",
            "0", "0", "0", "0", "1", "0", "0", "0",
            "0", "0", "0", "0", "2", "0", "0", "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
            "0", "0", "0", "0", "0", "0", "0", "0",
           ],
        revision: 0,
        selected: {
            name: "",
            value: 0
        }
    };

    // Function ---------------------------------------------
    // 初期化
    function init(board_size, rect_board, _ctx) {
        BOARD_SIZE = board_size;
        RECT_CANV  = rect_board;
        CELL_SIZE  = RECT_CANV.w / BOARD_SIZE | 0;
        ctx = _ctx;
        state = objCopy(init_state);
        setEvents();
        Render.render(ctx, state, point);
    }

    // イベントの関連付け
    function setEvents() {
        var isTouch;
        if ('ontouchstart' in window) {
            isTouch = true;
        } else {
            isTouch = false;
        }
        if (isTouch) {
            ctx.canvas.addEventListener('touchstart', ev_mouseClick)
        } else {
            ctx.canvas.addEventListener('mousemove', ev_mouseMove)
            ctx.canvas.addEventListener('mouseup', ev_mouseClick)
        }
    }

    // マウスカーソル移動のイベント処理
    function ev_mouseMove(e) {
        getMousePosition(e);
        state.selected = hitTest(point.x, point.y);
        Render.render(ctx, state, point);
    }

    // マウスクリックのイベント処理
    function ev_mouseClick(e) {
        var selected = hitTest(point.x, point.y);
        var number;
        //state.map = ApiController.get_gameboard_state()
        console.log(state.map); //非同期なので上手くいかない！

        if (selected.name === "RECT_CANV") {
            number = selected.value;
            Render.render(ctx, state, point);
            /*
            if (Ai.canPut(state.map, selected.value, state.turn) === true) {
                state.map = Ai.putMap(state.map, selected.value, state.turn);
                state.turn = -1 * state.turn;
                state.revision += 1;
                Render.render(ctx, state, point);

                setTimeout(function () {
                    var _number = Ai.thinkAI(state.map, state.turn, 6)[0];
                    state.map = Ai.putMap(state.map, _number, state.turn);
                    state.turn = -1 * state.turn;
                    state.revision += 1;
                    Render.render(ctx, state, point);
                }, 100);
            }
            */
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
        point.x = e.clientX - rect.left;
        point.y = e.clientY - rect.top;
    }

    // マウスカーソルの座標を取得する
    function hitTest(x, y) {
        var objects = [RECT_CANV];
        var click_obj = null;
        var selected = {
            name: "",
            value: 0
        }
        for (var i = 0; i < objects.length; i++) {
            if (objects[i].w >= x && objects[i].x <= x && objects[i].h >= y && objects[i].y <= y) {
                selected.name = "RECT_CANV";
                break;
            }
        }
        switch (true) {
        case selected.name === "RECT_CANV":
            selected.name = "RECT_CANV";
            selected.value = Math.floor(y / Render.CELL_SIZE) * BOARD_SIZE + Math.floor(x / Render.CELL_SIZE)
            break;
        }
        return selected;
    }

    // オブジェクトの実体をコピーする
    function objCopy(obj) {
        return JSON.parse(JSON.stringify(obj));
    }

})((this || 0).self || global);
