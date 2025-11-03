// Ant Design Vue 主题配置
export const antdTheme = {
  token: {
    // 主色调
    colorPrimary: '#4A90E2',
    colorSuccess: '#52C41A',
    colorWarning: '#FAAD14',
    colorError: '#FF4D4F',
    colorInfo: '#4A90E2',
    
    // 文字颜色
    colorText: '#333333',
    colorTextSecondary: '#666666',
    colorTextTertiary: '#999999',
    colorTextQuaternary: '#CCCCCC',
    
    // 背景色
    colorBgContainer: '#FFFFFF',
    colorBgElevated: '#FFFFFF',
    colorBgLayout: '#F5F7FA',
    colorBgSpotlight: '#E8F4FD',
    
    // 边框
    colorBorder: '#D9D9D9',
    colorBorderSecondary: '#E8E8E8',
    
    // 圆角
    borderRadius: 6,
    borderRadiusXS: 2,
    borderRadiusSM: 4,
    borderRadiusLG: 8,
    borderRadiusOuter: 4,
    
    // 字体
    fontSize: 14,
    fontSizeSM: 12,
    fontSizeLG: 16,
    fontSizeXL: 20,
    fontSizeHeading1: 38,
    fontSizeHeading2: 30,
    fontSizeHeading3: 24,
    fontSizeHeading4: 20,
    fontSizeHeading5: 16,
    
    // 行高
    lineHeight: 1.5714285714285714,
    lineHeightLG: 1.5,
    lineHeightSM: 1.66,
    
    // 间距
    padding: 16,
    paddingXS: 8,
    paddingSM: 12,
    paddingLG: 24,
    paddingXL: 32,
    
    margin: 16,
    marginXS: 8,
    marginSM: 12,
    marginLG: 24,
    marginXL: 32,
    
    // 阴影
    boxShadow: '0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05)',
    boxShadowSecondary: '0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05)',
    
    // 动画
    motionDurationFast: '0.1s',
    motionDurationMid: '0.2s',
    motionDurationSlow: '0.3s',
    
    // 控件高度
    controlHeight: 32,
    controlHeightSM: 24,
    controlHeightLG: 40,
    
    // 字重
    fontWeightStrong: 600,
    
    // 透明度
    opacityLoading: 0.65,
    
    // 链接颜色
    colorLink: '#4A90E2',
    colorLinkHover: '#357ABD',
    colorLinkActive: '#2E6BA8',
    
    // 填充颜色
    colorFill: 'rgba(0, 0, 0, 0.04)',
    colorFillSecondary: 'rgba(0, 0, 0, 0.06)',
    colorFillTertiary: 'rgba(0, 0, 0, 0.04)',
    colorFillQuaternary: 'rgba(0, 0, 0, 0.02)',
  },
  
  components: {
    // 按钮组件
    Button: {
      primaryColor: '#FFFFFF',
      defaultBg: '#FFFFFF',
      defaultBorderColor: '#D9D9D9',
      defaultColor: '#333333',
      dangerColor: '#FFFFFF',
      borderRadius: 4,
      controlHeight: 32,
      controlHeightLG: 40,
      controlHeightSM: 24,
      paddingInline: 15,
      paddingInlineLG: 15,
      paddingInlineSM: 7,
    },
    
    // 输入框组件
    Input: {
      borderRadius: 4,
      controlHeight: 32,
      controlHeightLG: 40,
      controlHeightSM: 24,
      paddingInline: 11,
      paddingInlineLG: 11,
      paddingInlineSM: 7,
      activeBorderColor: '#4A90E2',
      hoverBorderColor: '#4A90E2',
      activeShadow: '0 0 0 2px rgba(74, 144, 226, 0.2)',
    },
    
    // 选择器组件
    Select: {
      borderRadius: 4,
      controlHeight: 32,
      controlHeightLG: 40,
      controlHeightSM: 24,
      selectorBg: '#FFFFFF',
      optionSelectedBg: '#4A90E2',
      optionSelectedColor: '#FFFFFF',
      optionActiveBg: 'rgba(74, 144, 226, 0.1)',
      multipleItemBg: '#4A90E2',
      multipleItemBorderColor: '#4A90E2',
      multipleItemColor: '#FFFFFF',
    },
    
    // 日期选择器组件
    DatePicker: {
      borderRadius: 4,
      controlHeight: 32,
      controlHeightLG: 40,
      controlHeightSM: 24,
      cellActiveWithRangeBg: 'rgba(74, 144, 226, 0.1)',
      cellHoverBg: 'rgba(74, 144, 226, 0.1)',
      cellRangeBorderColor: '#4A90E2',
      cellBgDisabled: '#F5F5F5',
      timeColumnWidth: 56,
    },
    
    // 表单组件
    Form: {
      labelRequiredMarkColor: '#FF4D4F',
      labelColor: '#333333',
      labelFontSize: 14,
      itemMarginBottom: 24,
      verticalLabelPadding: '0 0 8px',
      verticalLabelMargin: 0,
    },
    
    // 复选框组件
    Checkbox: {
      borderRadius: 2,
      size: 16,
      colorPrimary: '#4A90E2',
    },
    
    // 单选框组件
    Radio: {
      size: 16,
      dotSize: 8,
      colorPrimary: '#4A90E2',
    },
    
    // 开关组件
    Switch: {
      colorPrimary: '#4A90E2',
      trackHeight: 22,
      trackMinWidth: 44,
      trackPadding: 2,
      handleSize: 18,
    },
    
    // 滑块组件
    Slider: {
      trackBg: 'rgba(0, 0, 0, 0.04)',
      trackHoverBg: 'rgba(0, 0, 0, 0.06)',
      railBg: 'rgba(0, 0, 0, 0.04)',
      railHoverBg: 'rgba(0, 0, 0, 0.06)',
      handleColor: '#4A90E2',
      handleActiveColor: '#357ABD',
      trackBgDisabled: 'rgba(0, 0, 0, 0.06)',
      handleColorDisabled: 'rgba(0, 0, 0, 0.25)',
      dotBorderColor: '#4A90E2',
      dotActiveBorderColor: '#357ABD',
    },
    
    // 上传组件
    Upload: {
      colorPrimary: '#4A90E2',
      colorPrimaryHover: '#357ABD',
    },
    
    // 评分组件
    Rate: {
      starColor: '#FADB14',
      starBg: 'rgba(0, 0, 0, 0.06)',
      starSize: 20,
      starHoverScale: 1.1,
    },
    
    // 卡片组件
    Card: {
      borderRadius: 6,
      paddingLG: 24,
      headerBg: 'transparent',
      headerFontSize: 16,
      headerFontSizeSM: 14,
      headerHeight: 56,
      headerHeightSM: 48,
    },
    
    // 消息组件
    Message: {
      borderRadius: 6,
      contentPadding: '10px 16px',
    },
    
    // 通知组件
    Notification: {
      borderRadius: 6,
      paddingVertical: 16,
      paddingHorizontal: 24,
    },
    
    // 模态框组件
    Modal: {
      borderRadius: 6,
      headerBg: '#FFFFFF',
      contentBg: '#FFFFFF',
      footerBg: 'transparent',
      titleFontSize: 16,
      titleLineHeight: 1.5,
    },
    
    // 抽屉组件
    Drawer: {
      borderRadius: 0,
      headerHeight: 56,
      bodyPadding: 24,
      footerPaddingBlock: 12,
      footerPaddingInline: 24,
    },
    
    // 表格组件
    Table: {
      borderRadius: 6,
      headerBg: '#FAFAFA',
      headerColor: '#333333',
      headerSortActiveBg: 'rgba(0, 0, 0, 0.04)',
      headerSortHoverBg: 'rgba(0, 0, 0, 0.04)',
      bodySortBg: 'rgba(0, 0, 0, 0.01)',
      rowHoverBg: 'rgba(0, 0, 0, 0.04)',
      rowSelectedBg: 'rgba(74, 144, 226, 0.04)',
      rowSelectedHoverBg: 'rgba(74, 144, 226, 0.08)',
    }
  }
}

// 导出默认主题配置
export default antdTheme