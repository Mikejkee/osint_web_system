$(function () {
    var formData = $("#taskForm");

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + '/view/';
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    socket.onmessage = function (e) {
      console.log("message: ", e);
      var data = JSON.parse(e.data);
      console.log(data)

      // if action is started, add new item to table
      if (data.action == "started") {
        var task_status = $("#task_status");
        var ele = $('<tr></tr>');
        var item_created = $("<td></td>").text(data.task_created);
        ele.append(item_created);
        var item_id = $("<td></td>").text(data.task_id);
        ele.append(item_id);
        var item_name = $("<td></td>").text(data.task_name);
        ele.append(item_name);
        var item_status = $("<td></td>");
        item_status.attr("id", "item-status-" + data.task_id);
        var span = $('<span class="badge badge-pill badge-warning"></span>').text(data.task_status);
        item_status.append(span);
        ele.append(item_status);
        task_status.append(ele);
      }
      // if action is completed, update the status
      else if (data.action == "completed") {
        var item = $('#item-status-' + data.task_id + ' span');
        item.attr("class", "badge badge-pill badge-success");
        item.text(data.task_status);
      }

    };
    socket.onopen = function (e) {
      console.log("open: ", e);

      formData.submit(function (event) {
        // Получаем все заполненные поля формы
        let serializeForm = getForm();
        event.preventDefault();

        // Отправляем по сокету нашему consumer-у
        socket.send(JSON.stringify(serializeForm));

        // Переходим на view к просомтру
        document.location.pathname = "/view";
        console.log("Saving value", serializeForm);
      })
    };
    socket.onerror = function (e) {
      console.log("error: ", e);
    };
    socket.onclose = function (e) {
      console.log("close: ", e);
    };
  });


function getForm() {
    return $('#taskForm').children().map(function () {
        if ($(this).find('input').attr('name')) {
            // Проходим по всем поляем формы, забираем их атрибут "name" где указан, по чем производится поиск,
            let searchType = $(this).find('input').attr('name');

            // Забираем значение этого поля
            let searchValue = $(this).find('input').val();

            // Забираем выбранные поля
            let serviceArr = $(this).find('div').find('label.active').map(function () {
                return [$(this).find('input').attr('id')]
            }).get();

            return {'search_type': searchType, 'search_value': searchValue, 'service_arr': serviceArr}
        }
    }).get()
}
// Старый види сбора формы
// function getForm1(form) {
//     let serializeForm = $(form).serializeArray();
//     serviceTypeArr = $('#taskForm label.active').map(function () {
//             return [$(this).find('input').attr('id')]
//         }).get();
//     serializeForm = serializeForm.concat({"name": "service_type", "values": serviceTypeArr})
//     return serializeForm
// };