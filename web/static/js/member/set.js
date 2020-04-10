;
var member_set_ops = {
    init:function () {

    },
    eventBind:function () {
        $('.wrap_member_set .save').click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass('disabled')){
                return;
            }

            var nickname_target = $('.wrap_member_set input[name=nickname]');
            var nickname = nickname_target.val();

            if (nickname.length < 1){
                common_ops.tip('昵称不能为空', nickname_target);
                return;
            }

            btn_target.addClass('disabled');
            var data = {
                nickname:nickname,
                id:$('.wrap_member_set input[name=id]').val()
            };

            $.ajax({
                url:common_ops.buildUrl('/member/set'),
                type:'POST',
                data:data,
                dataType:'json',
                success:function(res){
                    btn_target.removeClass('disabled');
                    var callback = undefined;
                    if(res.code == 200){
                        callback = function () {
                            window.location.href = common_ops.buildUrl('/member/index')
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });


        })
    }

};
$(document).ready({
    member_set_ops.init()
});