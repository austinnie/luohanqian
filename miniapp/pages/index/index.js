const app = getApp();

Page({
  onLoad: function() {
    // 加载历史记录
    app.loadHistory();
  },
  
  goToDraw: function() {
    wx.navigateTo({
      url: '/pages/draw/draw'
    });
  },  

  
  goToHistory: function() {
    wx.navigateTo({
      url: '/pages/history/history'
    });
  },
  
  // 新增关于页面跳转方法
  goToAbout() {
    wx.navigateTo({
      url: '/pages/about/about'
    });
  }
  
});