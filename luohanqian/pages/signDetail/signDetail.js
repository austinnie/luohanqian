// pages/signDetail/signDetail.js
const app = getApp();

Page({
  data: {
    sign: null,
	showFullAnalysis: true, // 默认展开
    analysisItems: [
      { key: 'career', title: '功名' },
      { key: 'marriage', title: '婚姻' },
      { key: 'wealth', title: '求财' },
      { key: 'health', title: '疾病' },
      { key: 'lawsuit', title: '诉讼' },
      { key: 'traveler', title: '行人' },
      { key: 'harvest', title: '年成' },
      { key: 'offspring', title: '求嗣' },
      { key: 'relocation', title: '移居' },
      { key: 'lost_property', title: '失物' },
      { key: 'travel', title: '出行' },
      { key: 'household', title: '家宅' },
      { key: 'pregnancy', title: '六甲' },
      { key: 'plans', title: '谋望' },
      { key: 'personal', title: '自身' }
    ]
  },
  
  toggleAnalysis() {
    this.setData({
      showFullAnalysis: !this.data.showFullAnalysis
    });
  },

	onLoad(options) {
	  // 方案1：尝试获取事件通道，如果不可用则直接使用参数
	  try {
		const eventChannel = this.getOpenerEventChannel();
		if (eventChannel && eventChannel.once) {
		  eventChannel.once('acceptSignData', (data) => {
			this.setData({ sign: data.sign });
		  });
		}
	  } catch (error) {
		console.warn('事件通道不可用:', error);
	  }

	  // 方案2：优先使用页面参数
	  if (options.signId) {
		this.loadSignFromGlobalData(options.signId);
	  }
	  
	  // 方案3：设置超时后备
	  setTimeout(() => {
		if (!this.data.sign && options.signId) {
		  this.loadSignFromGlobalData(options.signId);
		}
	  }, 500);
	},

  loadSignFromGlobalData(signId) {
    try {
      const sign = app.getSignByNumber(signId.replace('第', '').replace('签', ''));
      this.setData({ sign });
    } catch (error) {
      wx.showToast({
        title: '加载签文失败',
        icon: 'none'
      });
    }
  },

  formatLuckText(luck) {
    const luckMap = {
      'supreme_luck': '上上签（大吉）',
      'great_luck': '上吉签（吉）',
      'good_luck': '中吉签（小吉）',
      'neutral_luck': '中平签（平）',
      'bad_luck': '下下签（凶）'
    };
    return luckMap[luck] || '未知签运';
  },

  getLuckClass(luck) {
    const classMap = {
      'supreme_luck': 'luck-best',
      'great_luck': 'luck-good',
      'good_luck': 'luck-medium',
      'neutral_luck': 'luck-neutral',
      'bad_luck': 'luck-bad'
    };
    return classMap[luck] || '';
  },

  navigateBack() {
    wx.navigateBack();
  }
});