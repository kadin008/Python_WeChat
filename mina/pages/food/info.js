//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax:1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 4,
        commentCount:2
    },
    onLoad: function (e) {
        var that = this;

        that.setData({
            id: e.id
        })

        that.setData({
            commentList: [
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                },
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                }
            ]
        });

        that.getInfo();
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    addShopCar: function () {

    },
    buyNow: function () {
        wx.navigateTo({
            url: "/pages/order/index"
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if( this.data.buyNumber <= this.data.buyNumMin){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if( this.data.buyNumber >= this.data.buyNumMax ){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    getInfo: function () {
        var that = this;
        wx.request({
            url:app.buildUrl('/food/info'),
            header:app.getRequestHeader(),
            data:{
               id:that.data.id
            },
            success(res) {
                var resp = res.data;
                if (resp.code != 200){
                    app.alert({'content': resp.msg});
                    return;
                }
                 that.setData({
                     info: resp.data.info,
                     buyNumMax: resp.data.info.stock,
                });
                WxParse.wxParse('article', 'html', resp.data.info.summary, that, 5);
            }
        });

    }
});
