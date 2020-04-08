;
var user_edit_ops = {
    init:function () {
        this.eventBind();
    },
    eventBind: function () {
        $('.user_edit_wrap .save').click(function () {
            var btn_target = $(this);
            if(btn_target.hasClass('disabled')){
                common_ops.alert('正在处理中......')
                return;
            }

            var nickname_target = $('.user_edit_wrap input[name=nickname]');
            var nickname = nickname_target.val();

            var email_target = $('.user_edit_wrap input[name=email]');
            var email = email_target.val();

            if (!nickname || nickname.length < 2){
                common_ops.tip('', nickname_target);
                return false;
            }


        });

    }
};

$(document).ready(function () {
    user_edit_ops.init()

});







