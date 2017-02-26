/**
 *
 * Created by fly_l on 2017/2/20.
 */
$(document).ready(function(){

    $("#view_module>li>a").click(function() {
        var id = $(this).attr('id');
        console.log('/scan/' + id);
        $.get('/scan/'+id, function (result) {
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
    
    $('#task_info').click(a_fun);
    $("#add_module").click(a_fun);

    $("#new_single_task").click(a_fun);
    $("#new_batch_task").click(a_fun);

    $("#view_all_task").click(a_fun);
    $("#view_single_task").click(a_fun);
    $("#view_batch_task").click(a_fun);
    
    
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

