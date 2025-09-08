// pages/about/about.js
Page({
  data: {
    // 可以添加动态数据
  },

  onLoad() {
    // 页面加载时逻辑
  },

  navigateBack() {
    wx.navigateBack();
  },

  // 复制微信号功能
  copyWechat() {
    wx.setClipboardData({
      data: 'Austin_Japan',
      success: () => {
        wx.showToast({
          title: '微信号已复制',
          icon: 'success'
        });
      }
    });
  },

  // 复制邮箱功能
  copyEmail() {
    wx.setClipboardData({
      data: '爱行天下行者无疆',
      success: () => {
        wx.showToast({
          title: '微信公众号已复制',
          icon: 'success'
        });
      }
    });
  }
});