Page({
  data: {
    // 待上传的图片, 本地地址
    files: [],
    //下载的文件列表
    downloadedBackupedFiles:[]

  },
  chooseImage: function (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          files: that.data.files.concat(res.tempFilePaths)
        });
      }
    })
  },
  previewImage: function (e) {
    wx.previewImage({
      current: e.currentTarget.id, // 当前显示图片的http链接
      urls: this.data.files // 需要预览的图片http链接列表
    })
  },
  // 上传图片文件
  uploadpic: function () {
    for (var i = 0; i < this.data.files.length; i++) {
      var filePath = this.data.files[i]
      wx.uploadFile({
        url: 'http://127.0.0.1:8000/api/v1.0/apps/image1/',
        filePath: filePath,
        name: 'test'+filePath,
        success: function (res) {
          console.log(res.data),
            console.log(typeof (res.data))
        },
        fail:function(res){
          console.log(res.errMsg)
        },
      })
    }
  },
  // 下载图片
  loadpic: function (imgItem) {
    var that = this
    wx.downloadFile({
      url: 'http://127.0.0.1:8000/api/v1.0/apps/image1/',
      success: function (res) {
        console.log('成功了..')
        console.log(res.tempFilePath)
        console.log(res.filePath)
        var tmpPath = res.tempFilePath
        var newDownloadedBackupedFiles = that.data.downloadedBackupedFiles
        newDownloadedBackupedFiles.push(tmpPath)
        that.setData({
          downloadedBackupedFiles: newDownloadedBackupedFiles
        })
      }
    })
  },

  // 删除图片
  deletepic: function (imgItem) {
    wx.request({
      url: 'http://127.0.0.1:8000/api/v1.0/apps/image1/?name=a650.png',
      method: 'DELETE',
      success: function (res) {
        console.log(res.data)
        wx.showToast({
          title: res.data,
        })
      }
    })
  },

  // 长按确认删除函数
  longTapConfirm: function (e) {
    var that = this
    var confirmList = ["删除这个图片",'其他','sss']
    wx.showActionSheet({
      itemList: confirmList,
      success: function (res) {
        console.log('res:')
        console.log(res)
        if (res.tapIndex == 0) {
          console.log(confirmList[res.tapIndex])
          console.log(e)
          var imageIndex = e.currentTarget.dataset.index
          var imageItem = that.data.downloadedBackupedFiles[imageIndex]
          var newList = that.data.downloadedBackupedFiles
          newList.splice(imageIndex, 1)
          console.log(newList)
          that.setData({
            downloadedBackupedFiles: newList
          })
        // that.deletepic(imageItem)
        }else{
          console.log(confirmList[res.tapIndex])
          wx.showToast({
            title: '你选择了'+confirmList[res.tapIndex],
          })
        }
        
      }
    })
  },



});