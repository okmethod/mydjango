// 即時関数として定義
(function (global) { // globalオブジェクトを取得
  "use strict"; // strictモード
  // Class ------------------------------------------------
  function ApiController() {}

  // Header -----------------------------------------------
  global.ApiController = ApiController;
  global.ApiController.init = init
  global.ApiController.sendApiRequest   = sendApiRequest;

  // Const ------------------------------------------------
  var HOST_NAME;
  var GAME_PK;

  // Variable ---------------------------------------------
  var msg_div;

  // Function ---------------------------------------------
  // 初期化
  function init(_msg_div, host_name, game_pk) {
    msg_div   = _msg_div;
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

  // APIリクエストの送信
  function sendApiRequest(method, action, data={}) {
    return new Promise((resolve, reject) => {
      $.ajaxSetup({
        beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          }
        }
      });
      $.ajax({
        url: "http://" + host_name + "/reversi/api/game/" + game_pk + "/" + action,
        method: method,
        data: data,
      }).then(
        data => {
          //console.log(data);
          const msg = data.description;
          if (msg != null) {
            msg_div.textContent = msg;
          }
          resolve(data);
        },
        error => {
          console.log(error);
          const msg = error.responseJSON.description;
          if (msg != null) {
            msg_div.textContent = msg;
          }
          reject(error);
        }
      )
    })
  }

})((this || 0).self || global);
