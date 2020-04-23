//获取应用实例
var commonCityData = require('../../utils/city.js');
var app = getApp();
Page({
    data: {
        provinces: [],
        citys: [],
        districts: [],
        selProvince: '请选择',
        selCity: '请选择',
        selDistrict: '请选择',
        selProvinceIndex: 0,
        selCityIndex: 0,
        selDistrictIndex: 0
    },
    onLoad: function (e) {
        var that = this;
        this.initCityData(1);
    },
    //初始化城市数据
    initCityData:function( level, obj ){
        if (level == 1) {
            var pinkArray = [];
            for (var i = 0; i < commonCityData.cityData.length; i++) {
                pinkArray.push(commonCityData.cityData[i].name);
            }
            this.setData({
                provinces: pinkArray
            });
        } else if (level == 2) {
            var pinkArray = [];
            var dataArray = obj.cityList
            for (var i = 0; i < dataArray.length; i++) {
                pinkArray.push(dataArray[i].name);
            }
            this.setData({
                citys: pinkArray
            });
        } else if (level == 3) {
            var pinkArray = [];
            var dataArray = obj.districtList
            for (var i = 0; i < dataArray.length; i++) {
                pinkArray.push(dataArray[i].name);
            }
            this.setData({
                districts: pinkArray
            });
        }
    },
    bindPickerProvinceChange: function (event) {
        var selIterm = commonCityData.cityData[event.detail.value];
        this.setData({
            selProvince: selIterm.name,
            selProvinceIndex: event.detail.value,
            selCity: '请选择',
            selCityIndex: 0,
            selDistrict: '请选择',
            selDistrictIndex: 0
        });
        this.initCityData(2, selIterm);
    },
    bindPickerCityChange: function (event) {
        var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[event.detail.value];
        this.setData({
            selCity: selIterm.name,
            selCityIndex: event.detail.value,
            selDistrict: '请选择',
            selDistrictIndex: 0
        });
        this.initCityData(3, selIterm);
    },
    bindPickerChange: function (event) {
        var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].districtList[event.detail.value];
        if (selIterm && selIterm.name && event.detail.value) {
            this.setData({
                selDistrict: selIterm.name,
                selDistrictIndex: event.detail.value
            })
        }
    },
    bindCancel: function () {
        wx.navigateBack({});
    },
    bindSave: function (e) {
        var that = this;
        var nickname = e.detail.value.nickname;
        var address = e.detail.value.address;
        var mobile = e.detail.value.mobile;
        if(nickname == '' || nickname == undefined){
            app.tip({'content':'请填写联系人姓名'});
            return;
        }
        if (mobile == '' || mobile == undefined){
            app.tip({'content':'请填写联系人的手机号'})
            return;
        }
        if (that.data.selProvince == '请选择'){
            app.tip({'content':'请选择省份'})
            return;
        }
        if (that.data.selCity == '请选择'){
            app.tip({'content':'请选择省份'})
            return;
        }
        var city_id = commonCityData.cityData[that.data.selProvinceIndex].cityList[that.data.selCityIndex].id
        var district_id;
        if (that.data.selDistrict == '请选择' || !that.data.selDistrict){
            district_id = 0;
        }else{
            district_id = commonCityData.cityData[that.data.selProvinceIndex].cityList[that.data.selCityIndex].districtList[that.data.selDistrictIndex].id
        }
        if (address == '' || address == undefined) {
            app.tip({'content':'请输入详细地址'})
            return;
        }

        wx.request({
            url: app.buildUrl('/my/address/set'),
            header: app.getRequestHeader(),
            method: 'POST',
            data: {
                province_id: commonCityData.cityData[that.data.selProvinceIndex].id,
                province_str: that.data.selProvince,
                city_id: city_id,
                city_str: that.data.selCity,
                district_id: district_id,
                district_str: that.data.selDistrict,
                nickname: nickname,
                address: address,
                mobile: mobile,
            },
            success: function (res) {
                var resp = res.data;
                if (resp.code != 200){
                    app.alert({'content': resp.msg});
                    return;
                }
                wx.navigateBack({});
                
            }
        });

    },
    deleteAddress: function (e) {
    },
});
