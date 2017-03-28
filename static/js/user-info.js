/**
 * Created by fly_l on 2017/3/28.
 */

$(document).ready(function () {

    $(".head-tab>li>a").click(function () {
        var id = $(this).attr("id");
        $(".head-tab>li").removeClass('active');
        $(this).parent().addClass('active');
        // console.log(id);
        var tab_id = 'tab' + '-' + id.split('-')[1];
        // console.log(tab_id);
        $(".tab-content>.tab-panel").removeClass("active");
        $("#"+tab_id).addClass("active");
    });

    $("#password2").blur(function () {
        var pwd1 = $("#password1").val();
        var pwd2 = $("#password2").val();
        // console.log(pwd1);
        // console.log(pwd2);
        if (pwd1 != pwd2){
            $("#change-pwd-info").text("两次密码不相同，请重新输入");
            // $("#change-pwd-btn").attr({"disabled":"disabled"});
        }else{
            $("#change-pwd-btn").removeAttr("disabled");
        }
    });

});

var show_change_pwd_error = function (ret) {
    $("#change-pwd-info").text(ret);
};

var change_pwd_success = function () {
    alert("密码修改成功,请重新登录");
    // sleep(1);
    window.location='/user/login/';
};