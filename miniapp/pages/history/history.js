// pages/history/history.js
Page({
  data: {
    historyList: [],
    isEmpty: true,
    loading: true
  },

  onLoad() {
    this.loadHistory();
  },

  onShow() {
    // 当从详情页返回时刷新数据
    this.loadHistory();
  },

  loadHistory() {
    this.setData({ loading: true });
    
    const history = getApp().getHistory();
    this.setData({
      historyList: history,
      isEmpty: history.length === 0,
      loading: false
    });
  },

	// pages/history/history.js
	viewSignDetail(e) {
	  const sign = e.currentTarget.dataset.sign;
	
	  // 增强数据验证，支持从id中提取签号
	  if (!sign || !sign.id) {
		wx.showToast({ title: '签文数据异常', icon: 'none' });
		return;
	  }
	  
	  // 从id中提取数字签号（如从"第61签"中提取61）
	  const signNum = this.extractSignNumber(sign.id);
	  if (!signNum) {
		wx.showToast({ title: '签号格式错误', icon: 'none' });
		return;
	  }
	  
	  wx.navigateTo({
		url: `/pages/signDetail/signDetail?signId=${signNum}`,
		success: (res) => {
		  res.eventChannel.emit('acceptSignData', {
			sign: sign.fullSign || sign,
			fromHistory: true
		  });
		},
		fail: (err) => {
		  console.error('导航失败:', err);
		  wx.showToast({ title: '打开详情失败', icon: 'none' });
		}
	  });
	},
	
	// 添加从id中提取数字签号的方法
	extractSignNumber(idString) {
	  if (!idString) return null;
	  
	  // 支持多种格式："第61签"、"61"、61
	  const match = idString.match(/第?(\d+)签?/);
	  return match ? parseInt(match[1]) : null;
	},
	


	

  showClearConfirm() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有求签历史吗？此操作不可撤销',
      confirmColor: '#ff4444',
      success: (res) => {
        if (res.confirm) {
          getApp().clearHistory();
          this.loadHistory();
          wx.showToast({
            title: '已清空历史记录',
            icon: 'success'
          });
        }
      }
    });
  },

  navigateBack() {
    wx.navigateBack();
  },

  // 删除单条历史记录
  deleteHistoryItem(e) {
    const { index } = e.currentTarget.dataset;
    const item = this.data.historyList[index];
    
    wx.showModal({
      title: '确认删除',
      content: `确定要删除第${item.num}签的记录吗？`,
      success: (res) => {
        if (res.confirm) {
          getApp().removeFromHistory(index);
          this.loadHistory();
          wx.showToast({
            title: '已删除记录',
            icon: 'success'
          });
        }
      }
    });
  }
});