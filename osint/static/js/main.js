//Меню боковое
$(function () {
    /*--------- show and hide the menu  ---*/
    $('.button').on("click", function () {
        if ($('#body').hasClass('nav_is_visible') == true) {
            $('#body').removeClass('nav_is_visible');
            $('.button').removeClass('close');
        } else {
            $('#body').addClass('nav_is_visible');
            $('.button').addClass('close');
        }
    });

    $('#body').addClass('home_is_visible');

    function removeClasses() {
        $(".menu ul li").each(function () {
            let custom_class = $(this).find('a').data('class');
            $('#body').removeClass(custom_class);
        });
    }

    $('.menu a').on('click', function (e) {
        e.preventDefault();
        removeClasses();
        let custom_class = $(this).data('class');
        $('#body').addClass(custom_class);
    });
});
//
// <li>
//   <a href='#' data-class='home_is_visible'>Фамилия</a>
//   <label class="ios7-switch" style="font-size: 24px;">
//       <input type="checkbox" name="surname" value="text" about="Фамилия">
//       <span></span>
//   </label>
// </li>


// Form-search
$(function () {
    $('.tab-list li').click(function () {
        $(".tab-list li ").each(function () {
            $(this).removeClass('active');
        });
        $(this).addClass('active');
        let num_tab = $(this).find('a').attr('href').replace('#', '');
        $(".tab-pane").each(function () {
            if ($(this).attr('id') == num_tab) {
                $(this).addClass('active');
            } else {
                $(this).removeClass('active');
            }
        });
    });
});

// Календарь
$(function () {
    $('input[class="input--style-1 input-sf daterange"]').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        "locale": {
            "format": "DD.MM.YYYY",
            "customRangeLabel": "Свой",
            "daysOfWeek": [
                "Вс",
                "Пн",
                "Вт",
                "Ср",
                "Чт",
                "Пт",
                "Сб"
            ],
            "monthNames": [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь"
            ],
            "firstDay": 1
        }
    }, function (start, end, label) {
        console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
    });
});

// Кнопка удалиьть напротив строк в таблице просмотра
function deleteStr(str) {
    console.log(str);
    $(str).hide(500);
}


// Отправка формы поиска
// $(function() {
//     $('#search_submit').click(function() {
//         $.ajax({
//             type: 'POST',
//             data: $('#search_form').serialize(),
//             success: function(data) {
//                 console.log(data);
//                 window.location.href = "http://127.0.0.1:8000/view/person"
//                 // window.setTimeout(function(){location.reload()},3000)
//             }
//         });
// });
// });
