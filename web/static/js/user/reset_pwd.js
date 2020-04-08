;
var mod_pwd_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind: function () {
        $('#save').click(function () {
            var btn_target = $(this);
            if(btn_target.hasClass('disabled')){
                common_ops.alert('正在处理中......')
                return;
            }

            var old_password = $('#old_password').val();
            var new_password = $('#new_password').val();

            if (!old_password){
                common_ops.alert('请输入原密码');
                return false;
            }

            if (!new_password || email.length < 8){
                common_ops.alert('请输入不少于8位的新密码');
                return false;
            }

            var data = {
                old_password: old_password,
                new_password: new_password
            }

            btn_target.addClass('disabled');
            $.ajax({
                url:common_ops.buildUrl('/user/reset-pwd'),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disabled')
                    var callback = null;
                    if(res.code == 200){
                        callback = function(){
                             window.location.href = window.location.href
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })

        });

    }
};

$(document).ready(function () {
    mod_pwd_ops.init()

});






