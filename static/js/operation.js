/**
 *
 * Created by fly_l on 2017/2/20.
 */


$("#sidebar-list>li>a").click(function(){
// 　　获取到当前点击的a标签的文本
//     console.log($(this).attr('href'))
    var class_name = $(this).attr('class')
    if (class_name == 'scan'){
        var a=$(this).attr('id');
        console.log('/scan/' + a);
        $.get('/scan/'+a, function (result) {
            $("#content").html(result);
        });
    }else{
        var a=$(this).attr('id');
        console.log('/'+a);
        $.get('/'+a, function (result) {
            $("#content").html(result);
        });
    }
});

$("#show_task>li>a").click(function() {
    var class_name = $(this).attr('class')
    if (class_name == 'task') {
        var a = $(this).attr('id');
        console.log('/task/' + a);
        $.get('/task/' + a, function (result) {
            $("#content").html(result);
        });
    } else if (class_name == 'batch') {
        var a = $(this).attr('id');
        console.log('/batch/' + a);
        $.get('/batch/' + a, function (result) {
            $("#content").html(result);
        });
    }
});

$("#task_button>li>a").click(function() {
    var a=$(this).attr('id');
    if (a == 'task-listbox'){
        return;
    }
    console.log('/' + a);
    $.get('/'+a, function (result) {
        $("#content").html(result);
    });
});