$("#taskForm").submit(function (event) {
    // Забираем имя пользователя работающего в системе
    let userName = $(document).find('#django_user').text()

    // Получаем данные формы и кладем в локальный сторедж для дальнейшей отправки через сокет
    let serializeForm = JSON.stringify(getForm(userName));
    event.preventDefault();
    localStorage.setItem('taskForm', serializeForm);

    // Переходим на просмотр 
    document.location.pathname = "/view/";
    console.log("Saving value", eval(serializeForm));
});

$(function () {
    if (document.location.pathname === "/view/") {
        // Устанавливаем коннект с сокетом
        let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
        let ws_path = ws_scheme + '://' + window.location.host + '/view/';
        console.log("Connecting to " + ws_path);
        let socket = new ReconnectingWebSocket(ws_path);
        console.log(socket);

        // Когда приходит сообщение
        socket.onmessage = function (e) {
            console.log("message: ", e);

            // Парсим json
            let data = JSON.parse(e.data);
            console.log(data);

            // Если задача со статусом "started", отрисовываем новую строку в таблице
            if (data.action === "started") {
                let task_status = $("#task_status");
                let ele = $('<tr></tr>');
                let item_created = $("<td></td>").text(data.task_created);
                ele.append(item_created);
                let item_id = $("<td></td>").text(data.task_type);
                ele.append(item_id);
                let item_name = $("<td></td>").text(data.task_name);
                ele.append(item_name);
                let item_status = $("<td></td>");
                item_status.attr("id", "item-status-" + data.task_id);
                let span = $('<span class="badge badge-pill badge-warning"></span>').text(data.task_status);
                item_status.append(span);
                ele.append(item_status);
                task_status.append(ele);
            }
            // Если задача со статусом "completed", меняем статус и отрисовываем информацию
            else if (data.action === "completed") {
                let item = $('#item-status-' + data.task_id + ' span');
                item.attr("class", "badge badge-pill badge-success");
                item.text(data.task_status);

                // Визуализируем
                console.log(data.service_result);
                visualization(data.service_result);
            }
        };
        socket.onopen = function (e) {
            console.log("open: ", e);

            // Достаем форму поиска
            let serializeForm = eval(localStorage.taskForm);

            // Отправляем ее по сокету и очищаем localStorage
            if (serializeForm) {
                socket.send(JSON.stringify(serializeForm));
                delete localStorage.taskForm;
            }
        };

        socket.onerror = function (e) {
            console.log("error: ", e);
        };

        socket.onclose = function (e) {
            console.log("close: ", e);
        };
    }

});


function getForm(userName) {
    return $('#taskForm').children().map(function () {
        if ($(this).find('input').attr('name')) {

            // Проходим по всем поляем формы, забираем их атрибут "name" где указан, по чем производится поиск и значение
            let searchTypeValue = {};
            $(this).find('.form-control').each(function () {
                searchTypeValue[$(this).attr('name')] = $(this).val();
            });

            // Забираем название сервиса
            let serviceName = $(this).find('div').find('label.active').find('input').attr('id').split("_");
            let search_type = serviceName[0];
            serviceName = serviceName[1].replace(/([a-z])([A-Z])/g, '$1 $2');

            return {'search_parameters': searchTypeValue, 'service_name': serviceName, 'search_type': search_type, 'userName': userName}
        }
    }).get()
}

function getNeo4jData() {
    let post_request = {"statements":[{"statement":"match (n)-[r]-() return r;", "resultDataContents":["graph"]}]};
    $.ajax({
      type: "POST",
      accept: "application/json",
      contentType:"application/json; charset=utf-8",
      url: "http://localhost:7474/db/data/transaction/commit",
      data: JSON.stringify(post_request),
      success: function(data, textStatus, jqXHR){
        console.log(data);
        draw_neo4j_graph(data);
        },
      failure: function(msg){console.log("failed")}
    });

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