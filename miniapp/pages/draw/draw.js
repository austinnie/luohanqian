// pages/draw/draw.js
const app = getApp();

Page({
  data: {
    animationData: {},
    sign: null,
    isDrawing: false,
    showDetails: false,
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
    ],
    currentAnimation: null
  },

  onLoad() {
    this.luckTextMap = {
      'supreme_luck': '上上签（大吉）',
      'great_luck': '上吉签（吉）',
      'good_luck': '中吉签（小吉）',
      'neutral_luck': '中平签（平）',
      'bad_luck': '下下签（凶）'
    };
  },

  onUnload() {
    // 清除动画防止内存泄漏
	this.setData({ currentAnimation: null });
  },

  startDraw() {
    if (this.data.isDrawing) return;
    
    this.setData({ 
      isDrawing: true,
      showDetails: false,
      sign: null
    });

    const animation = wx.createAnimation({
      duration: 2000,
      timingFunction: 'ease-in-out'
    });
    
    // 更流畅的动画效果
    animation.rotate(360).scale(1.2).step({ duration: 1000 });
    animation.rotate(-360).scale(0.8).step({ duration: 500 });
    animation.rotate(0).scale(1).step({ duration: 500 });
    
    this.setData({ 
      animationData: animation.export(),
      currentAnimation: animation
    });

    // 模拟抽签过程
    setTimeout(() => {
      const sign = app.drawRandomSign();
      if (sign) {
        const signNum = this.extractSignNumber(sign.id);
        
        const historySign = {
          id: sign.id,
          num: signNum,
          poem: sign.poem,
          summary: sign.summary,
          luck: sign.luck,
          analysis: sign.analysis || this.generateDefaultAnalysis(sign.luck),
          time: new Date().toLocaleString()
        };
        
        app.addToHistory(historySign);
        this.setData({ 
          sign: historySign,
          showDetails: true
        });
      }
      this.setData({ isDrawing: false });
    }, 2000);
  },

  extractSignNumber(idString) {
    const match = idString.match(/第(\d+)签/);
    return match ? parseInt(match[1]) : null;
  },

  generateDefaultAnalysis(luck) {
    const defaultText = {
      'supreme_luck': '大吉，诸事顺遂',
      'great_luck': '吉，运势良好',
      'good_luck': '小吉，平稳发展',
      'neutral_luck': '平，需谨慎行事',
      'bad_luck': '凶，宜守不宜进'
    };
    
    return this.data.analysisItems.reduce((result, item) => {
      result[item.key] = defaultText[luck] || '--';
      return result;
    }, {});
  },

  toggleDetails() {
    this.setData({
      showDetails: !this.data.showDetails
    });
  },

  getLuckClass(luck) {
    const luckClasses = {
      'supreme_luck': 'luck-best',
      'great_luck': 'luck-good',
      'good_luck': 'luck-medium',
      'neutral_luck': 'luck-neutral',
      'bad_luck': 'luck-bad'
    };
    return luckClasses[luck] || '';
  },

	// 在draw.js中添加
	saveSign() {
	  if (!this.data.sign) {
		wx.showToast({ title: '暂无签文可保存', icon: 'none' });
		return;
	  }
	  
	  const signData = {
		id: this.data.sign.id,
		num: this.extractSignNumber(this.data.sign.id),
		poem: this.data.sign.poem,
		summary: this.data.sign.summary,
		luck: this.data.sign.luck
	  };

	  if (getApp().saveSign(signData)) {
		wx.showToast({ title: '签文已保存', icon: 'success' });
	  } else {
		wx.showToast({ title: '该签文已存在', icon: 'none' });
	  }
	},


  viewSignDetail() {
    if (!this.data.sign) return;
    
    wx.navigateTo({
      url: `/pages/signDetail/signDetail?signId=${this.data.sign.id}&signNum=${this.data.sign.num}`,
      success: (res) => {
        res.eventChannel.emit('acceptSignData', {
          sign: this.data.sign,
          fromHistory: false
        });
      }
    });
  },

  drawAgain() {
    this.setData({ 
      sign: null,
      showDetails: false
    });
  }
});