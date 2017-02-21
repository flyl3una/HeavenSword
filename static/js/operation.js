/**
 *
 * Created by fly_l on 2017/2/20.
 */
$(document).ready(function(){

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
            a = a.split('-')[1]
            console.log('/show_task/' + a);
            $.get('/show_task/' + a, function (result) {
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

    fun = function() {
        var a=$(this).attr('id');
        console.log('/' + a);
        $.get('/'+a, function (result) {
            $("#content").html(result);
        });
    };

    $("#task_list").click(fun);
    $("#new_task>li>a").click(fun);

});


$(document).ready(function() {
    //icheck插件
    icheck = function () {
        $('input').iCheck({
            checkboxClass: 'icheckbox_minimal-blue',
            radioClass: 'iradio_minimal-blue',
            increaseArea: '20%' // optional
        });
    };
});
