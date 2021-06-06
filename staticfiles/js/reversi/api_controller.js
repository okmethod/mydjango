// 即時関数として定義
(function (global) { // globalオブジェクトを取得
    "use strict"; // strictモード
    // Class ------------------------------------------------
    function ApiController() {}

    // Header -----------------------------------------------
    global.ApiController = ApiController;
    global.ApiController.init = init
    global.ApiController.getGameState   = getGameState;
    global.ApiController.restartGame    = restartGame;
    global.ApiController.postGameRecord = postGameRecord;

    // Const ------------------------------------------------
    var HOST_NAME;
    var GAME_PK;

    // Function ---------------------------------------------
    // 初期化
    function init(host_name, game_pk) {
        HOST_NAME = host_name;
        GAME_PK   = game_pk;
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    // ゲームの公開情報の開示を要求
    function getGameState() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: "http://" + host_name + "/reversi/api/game/" + game_pk,
                method: "GET",
                data: {},
            }).then(
                data => {
                  //console.log(data);
                  resolve(data);
                },
                error => {
                  console.log(error);
                  reject(error);
                }
            )
        })
    }

    // ゲームの初期化を要求
    function restartGame() {
        return new Promise((resolve, reject) => {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                }
            });
            $.ajax({
                url: "http://" + host_name + "/reversi/api/game/" + game_pk + "/restart_game/",
                method: "PATCH",
                data: {},
            }).then(
                data => {
                  //console.log(data);
                  resolve(data);
                },
                error => {
                  console.log(error);
                  reject(error);
                }
            )
        })
    }

    // プレイヤーアクションの施行を要求
    function postGameRecord(player_pk, action, pos) {
        return new Promise((resolve, reject) => {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                }
            });
            $.ajax({
                url: "http://" + host_name + "/reversi/api/record/try_player_action/",
                method: "POST",
                data: {"game":game_pk, "player":player_pk,
                       "action":action, "pos_x":pos.x, "pos_y":pos.y,},
            }).then(
                data => {
                  //console.log(data);
                  resolve(data);
                },
                error => {
                  console.log(error);
                  reject(error);
                }
            )
        })
    }

})((this || 0).self || global);
