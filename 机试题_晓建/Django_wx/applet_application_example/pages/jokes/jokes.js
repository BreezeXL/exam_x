// pages/jokes/jokes.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    content:[]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
    var timestamp = Date.parse(new Date())/1000;
    console.log(timestamp)
    var that = this
    wx.request({
      // todo: 如何将关键信息放到本地配置文件读取
      // 解决思路 1 读取小程序的自定义配置参数
      // 2 如果不可以,就读取自定义本地配置文件
      // this.readfile2() 没成功
      // 3 如果也不可以,获取远端参数
      url: 'http://v.juhe.cn/joke/content/list.php?sort=desc&page=1&pagesize=5&time=' + timestamp+'&key=a3d4e42ae7d867b78774ca35f741f124',
      success:function(res){
        console.log(res.data)
        // # 数据请求成功了,更新到前台界面
        that.setData({
          content:res.data.result.data
        })

      }
    })
  },
  
  

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    wx.updateShareMenu({
      withShareTicket: true,
      success() { }
    })
  }
})