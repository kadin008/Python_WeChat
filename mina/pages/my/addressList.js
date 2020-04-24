//获取应用实例
var app = getApp();
Page({
    data: {
        addressList: []
    },
    selectTap: function (e) { 
        // 选中谁就把谁设置为默认的
        var that = this;
        wx.request({
          url: app.buildUrl('/my/address/ops'),
          header: app.getRequestHeader(),
          method: 'POST',
          data: {
            id: e.currentTarget.dataset.id,
            act: 'default'
          },
          success: function(res){
            var resp = res.data;
            if (resp.code != 200){
              app.alert({'content': resp.msg});
              return;
            }
            that.setData({
                addressList:resp.data.list
            })
          }
        });

        //从商品详情下单选择地址之后返回
        wx.navigateBack({});
    },
    addessSet: function (e) {
        wx.navigateTo({
            url: "/pages/my/addressSet?id=" + e.currentTarget.dataset.id
        })
    },
    onShow: function () {
        var that = this;
        that.getList();
    },
    getList: function(){
        var that = this;
        wx.request({
          url: app.buildUrl('/my/address/list'),
          header: app.getRequestHeader(),
          method: 'POST',
          success: function(res){
              var resp = res.data;
              if (resp.code != 200){
                app.alert({'content': resp.msg});
                return;
              }
              that.setData({
                addressList: resp.data.list
              });
          }
        })
    }
});
