/**
 *
 * Created by fly_l on 2017/2/20.
 */
$(document).ready(function(){

    $("#view_module>li>a").click(function() {
        var id = $(this).attr('id');
        console.log('/tools/' + id);
        $.get('/tools/'+id, function (result) {
            $("#content").html(result);
        });
    });

    var a_fun = function() {
        var a=$(this).attr('id');
        var href = $(this).attr('href');
        console.log('/' + a);
        $.get('/'+a, function (result) {
            $("#content").html(result);
        });
    };

    var tools_fun = function() {
        var a=$(this).attr('id');
        var href = $(this).attr('href');
        console.log('/' + a);
        $.get('/tools/'+a, function (result) {
            $("#content").html(result);
        });
    };

    var xx = function () {
        consolo.log("xx");
    };

    // $('.current-task-info').click(function () {
    //     var a=$(this).attr('id');
    //     var id = a.split('-')[1];
    //     console.log(id);
    //     if(id == '0'){
    //         $("#content").html('<h3>请先创建任务</h3>');
    //     }
    //     else{
    //         $.get('/web_task_info/'+id, function (result) {
    //             $("#content").html(result);
    //         });
    //     }
    // });

    $("#help").click(a_fun);

    $("#add_module").click(a_fun);

    $(".web_task").click(a_fun);
    // $("#new_single_web_task").click(a_fun);
    // $("#new_batch_web_task").click(a_fun);
    // $("#view_web_task_list").click(a_fun);
    $(".sys_task").click(a_fun);
    // $("#new_single_sys_task").click(a_fun);
    // $("#new_batch_sys_task").click(a_fun);
    // $("#view_sys_task_list").click(a_fun);

    $(".tools-a").click(tools_fun);

    // $("#port_scan").click(tools_fun);
    // $("#web_spider").click(tools_fun);
    // $("#domain_brute").click(tools_fun);


    // //icheck插件
    // icheck = function () {
    //     $('input').iCheck({
    //         checkboxClass: 'icheckbox_minimal-blue',
    //         radioClass: 'iradio_minimal-blue',
    //         increaseArea: '20%' // optional
    //     });
    // };
    // $('input').iCheck(icheck());
});


//定义js函数不要在ready里面定义。
// var form_result = function(ret) {
//     console.log(ret);
//     $("#port_scan_form_result").html(ret);
// };


