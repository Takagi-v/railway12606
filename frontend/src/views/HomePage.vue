<template>
  <div class="railway-homepage">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-container">
        <!-- Logo和搜索区域 -->
        <div class="header-top">
          <div class="logo-section">
            <h1 class="logo">
              <router-link to="/" class="logo-link">中国铁路12306</router-link>
            </h1>
          </div>
          
          <div class="search-section">
            <div class="search-box">
              <input 
                type="text" 
                placeholder="搜索车票、餐饮、常旅客、相关规章"
                class="search-input"
                v-model="searchKeyword"
              />
              <button class="search-btn" @click="handleGlobalSearch">
                <SearchOutlined />
              </button>
            </div>
          </div>
          
          <!-- 顶部右侧导航 -->
          <nav class="top-nav">
            <a href="#" class="nav-link">无障碍</a>
            <span class="nav-separator">|</span>
            <a href="#" class="nav-link">敬老版</a>
            <span class="nav-separator">|</span>
            <div class="nav-dropdown">
              <a href="#" class="nav-link dropdown-trigger">
                English
                <DownOutlined class="dropdown-icon" />
              </a>
            </div>
            <span class="nav-separator">|</span>
            <div class="nav-dropdown">
              <a href="#" @click.prevent="handleMyAccount" class="nav-link dropdown-trigger">
                我的12306
                <DownOutlined class="dropdown-icon" />
              </a>
            </div>
            <span class="nav-separator">|</span>
            <div class="auth-links">
              <a href="#" @click.prevent="handleLogin" class="nav-link">登录</a>
              <a href="#" @click.prevent="handleRegister" class="nav-link">注册</a>
            </div>
          </nav>
        </div>
        
        <!-- 主导航菜单 -->
        <nav class="main-nav">
          <ul class="nav-menu">
            <li class="nav-item active">
              <router-link to="/" class="nav-link" @click="handleMainNavClick('首页')">首页</router-link>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('车票')" class="nav-link dropdown-trigger">
                车票
                <DownOutlined class="dropdown-icon" />
              </a>
              <div class="dropdown-menu">
                <a href="#" class="dropdown-item">购买</a>
                <a href="#" class="dropdown-item">变更</a>
                <a href="#" class="dropdown-item">更多</a>
              </div>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('团购服务')" class="nav-link dropdown-trigger">
                团购服务
                <DownOutlined class="dropdown-icon" />
              </a>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('会员服务')" class="nav-link dropdown-trigger">
                会员服务
                <DownOutlined class="dropdown-icon" />
              </a>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('站车服务')" class="nav-link dropdown-trigger">
                站车服务
                <DownOutlined class="dropdown-icon" />
              </a>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('商旅服务')" class="nav-link dropdown-trigger">
                商旅服务
                <DownOutlined class="dropdown-icon" />
              </a>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('出行指南')" class="nav-link dropdown-trigger">
                出行指南
                <DownOutlined class="dropdown-icon" />
              </a>
            </li>
            <li class="nav-item dropdown">
              <a href="#" @click.prevent="handleMainNavClick('信息查询')" class="nav-link dropdown-trigger">
                信息查询
                <DownOutlined class="dropdown-icon" />
              </a>
              <div class="dropdown-menu">
                <a href="#" class="dropdown-item">常用查询</a>
              </div>
            </li>
          </ul>
        </nav>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 轮播图和搜索表单合并区域 -->
      <div class="carousel-search-section">
        <div class="carousel-container">
          <!-- 轮播图背景 -->
          <div class="carousel-background">
            <!-- 轮播图片 -->
            <div class="carousel-slides">
              <div 
                v-for="(item, index) in carouselItems" 
                :key="item.id"
                :class="['carousel-slide', { active: currentSlide === index }]"
                :style="{ backgroundImage: `url(${item.image})` }"
              >
                <div class="slide-overlay"></div>
              </div>
            </div>
            
            <div class="carousel-indicators">
              <span 
                v-for="(item, index) in carouselItems" 
                :key="index"
                :class="['indicator', { active: currentSlide === index }]"
                @click="handleIndicatorClick(index)"
              >
                {{ index + 1 }}
              </span>
            </div>
          </div>
          
          <!-- 车票搜索表单 - 内嵌在左半部分 -->
          <div class="embedded-search-form">
            <div class="search-form-header">
              <div class="service-tabs">
                <div class="tab-item active">
                  <CarOutlined />
                  车票
                </div>
                <div class="tab-item">
                  <SearchOutlined />
                  常用查询
                </div>
                <div class="tab-item">
                  <ShoppingOutlined />
                  订餐
                </div>
              </div>
            </div>

            <div class="search-tabs">
              <div 
                v-for="tab in searchTabs" 
                :key="tab.key"
                :class="['search-tab', { active: activeTab === tab.key }]"
                @click="handleTabChange(tab.key)"
              >
                <component :is="tab.icon" class="tab-icon" />
                {{ tab.label }}
              </div>
            </div>

            <div class="search-form">
              <div class="form-row">
                <div class="input-group">
                  <label class="input-label">出发地</label>
                  <div class="input-wrapper">
                    <input 
                      type="text" 
                      v-model="searchForm.fromStation"
                      placeholder="请输入或选择出发地"
                      class="station-input"
                    />
                    <EnvironmentOutlined class="input-icon" />
                  </div>
                </div>

                <div class="input-group">
                  <label class="input-label">到达地</label>
                  <div class="input-wrapper">
                    <input 
                      type="text" 
                      v-model="searchForm.toStation"
                      placeholder="请输入或选择到达地"
                      class="station-input"
                    />
                    <EnvironmentOutlined class="input-icon" />
                  </div>
                </div>

                <div class="swap-btn" @click="swapStations">
                  <SwapOutlined />
                </div>
              </div>

              <div class="form-row">
                <div class="input-group">
                  <label class="input-label">出发日期</label>
                  <div class="input-wrapper">
                    <input 
                      type="text" 
                      v-model="searchForm.departureDate"
                      placeholder="请输入日期"
                      class="date-input"
                      readonly
                      @click="showDatePicker = true"
                    />
                    <CalendarOutlined class="input-icon" />
                  </div>
                </div>

                <div class="input-group" v-if="activeTab === 'round'">
                    <label class="input-label">返程日期</label>
                    <div class="input-wrapper">
                      <input 
                        type="text" 
                        v-model="searchForm.returnDate"
                        placeholder="请输入返程日期"
                        class="date-input"
                        readonly
                        @click="showReturnDatePicker = true"
                      />
                      <CalendarOutlined class="input-icon" />
                    </div>
                  </div>

                  <!-- 返程日期选择器 -->
                  <div v-if="showReturnDatePicker" class="date-picker-overlay" @click="showReturnDatePicker = false">
                    <div class="date-picker" @click.stop>
                      <div class="date-picker-header">
                        <h3>选择返程日期</h3>
                        <button @click="showReturnDatePicker = false" class="close-btn">×</button>
                      </div>
                      <div class="date-picker-content">
                        <div class="date-grid">
                          <div 
                            v-for="date in availableDates" 
                            :key="date"
                            class="date-item"
                            :class="{ selected: searchForm.returnDate === date }"
                            @click="handleReturnDateSelect(date)"
                          >
                            {{ dayjs(date).format('MM-DD') }}
                            <span class="weekday">{{ dayjs(date).format('ddd') }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                <div class="search-options">
                  <label class="option-item">
                    <input type="checkbox" v-model="searchForm.isStudent" />
                    学生
                  </label>
                  <label class="option-item">
                    <input type="checkbox" v-model="searchForm.isHighSpeed" />
                    高铁/动车
                  </label>
                </div>

                <button class="search-button" @click="handleTicketSearch">
                  查&nbsp;&nbsp;&nbsp;&nbsp;询
                </button>
              </div>

              <!-- 搜索历史 -->
              <div class="search-history" v-if="searchHistory.length > 0">
                <div class="history-header">
                  <HistoryOutlined />
                  <span class="history-routes">
                    <span 
                      v-for="(route, index) in searchHistory" 
                      :key="index"
                      class="history-route"
                      @click="selectHistoryRoute(route)"
                    >
                      {{ route }}
                    </span>
                  </span>
                  <a href="#" class="clear-history" @click="clearHistory">删除历史</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷服务图标 -->
      <div class="service-icons">
        <div class="service-item" v-for="service in quickServices" :key="service.name" @click="handleServiceClick(service.name)">
          <div class="service-icon">
            <component :is="service.icon" />
          </div>
          <span class="service-name">{{ service.name }}</span>
        </div>
      </div>

      <!-- 公告区域 -->
      <div class="announcements">
        <div class="announcement-tabs">
          <div 
            class="tab" 
            :class="{ active: activeAnnouncementTab === 'latest' }"
            @click="activeAnnouncementTab = 'latest'"
          >
            最新发布
          </div>
          <div 
            class="tab" 
            :class="{ active: activeAnnouncementTab === 'faq' }"
            @click="activeAnnouncementTab = 'faq'"
          >
            常见问题
          </div>
          <div 
            class="tab" 
            :class="{ active: activeAnnouncementTab === 'credit' }"
            @click="activeAnnouncementTab = 'credit'"
          >
            信用信息
          </div>
        </div>
        
        <div class="announcement-list">
          <div 
            v-for="announcement in currentAnnouncements" 
            :key="announcement.id"
            class="announcement-item"
            @click="handleAnnouncementClick(announcement)"
          >
            <span class="announcement-type">{{ announcement.type }}</span>
            <a href="#" class="announcement-title" @click.prevent>{{ announcement.title }}</a>
            <span class="announcement-date">{{ announcement.date }}</span>
          </div>
          <div class="more-link">
            <a href="#" @click.prevent="handleMoreAnnouncements">更多></a>
          </div>
        </div>
      </div>
    </main>

    <!-- 页面底部 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-main">
          <div class="footer-section">
            <h4>购票服务</h4>
            <div class="footer-links">
              <a href="#" @click.prevent="handleFooterLink('购票')">购票</a>
              <a href="#" @click.prevent="handleFooterLink('改签')">改签</a>
              <a href="#" @click.prevent="handleFooterLink('退票')">退票</a>
              <a href="#" @click.prevent="handleFooterLink('候补购票')">候补购票</a>
              <a href="#" @click.prevent="handleFooterLink('时刻表')">时刻表</a>
              <a href="#" @click.prevent="handleFooterLink('正晚点')">正晚点</a>
            </div>
          </div>
          
          <div class="footer-section">
            <h4>信息查询</h4>
            <div class="footer-links">
              <a href="#" @click.prevent="handleFooterLink('余票查询')">余票查询</a>
              <a href="#" @click.prevent="handleFooterLink('订单查询')">订单查询</a>
              <a href="#" @click.prevent="handleFooterLink('积分查询')">积分查询</a>
              <a href="#" @click.prevent="handleFooterLink('会员服务')">会员服务</a>
              <a href="#" @click.prevent="handleFooterLink('客服中心')">客服中心</a>
              <a href="#" @click.prevent="handleFooterLink('投诉建议')">投诉建议</a>
            </div>
          </div>
          
          <div class="footer-section">
            <h4>旅客服务</h4>
            <div class="footer-links">
              <a href="#" @click.prevent="handleFooterLink('重点旅客')">重点旅客</a>
              <a href="#" @click.prevent="handleFooterLink('失物招领')">失物招领</a>
              <a href="#" @click.prevent="handleFooterLink('站车服务')">站车服务</a>
              <a href="#" @click.prevent="handleFooterLink('便民服务')">便民服务</a>
              <a href="#" @click.prevent="handleFooterLink('约车服务')">约车服务</a>
              <a href="#" @click.prevent="handleFooterLink('托运服务')">托运服务</a>
            </div>
          </div>
          
          <div class="footer-section">
            <h4>友情链接</h4>
            <div class="footer-links">
              <a href="#" @click.prevent="handleFooterLink('中国铁路')">中国铁路</a>
              <a href="#" @click.prevent="handleFooterLink('铁路客服')">铁路客服</a>
              <a href="#" @click.prevent="handleFooterLink('铁路货运')">铁路货运</a>
              <a href="#" @click.prevent="handleFooterLink('中铁快运')">中铁快运</a>
              <a href="#" @click.prevent="handleFooterLink('高铁网')">高铁网</a>
              <a href="#" @click.prevent="handleFooterLink('铁路论坛')">铁路论坛</a>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <div class="footer-qr">
            <div class="qr-section">
              <div class="qr-code">
                <div class="qr-placeholder">
                  📱
                </div>
              </div>
              <span>中国铁路官方微信</span>
            </div>
            <div class="qr-section">
              <div class="qr-code">
                <div class="qr-placeholder">
                  🚄
                </div>
              </div>
              <span>铁路12306</span>
            </div>
          </div>
          
          <div class="footer-info">
            <p>© 2024 中国铁路客户服务中心 版权所有</p>
            <p>
              <a href="#" @click.prevent="handleFooterLink('网站声明')">网站声明</a>
              <a href="#" @click.prevent="handleFooterLink('法律声明')">法律声明</a>
              <a href="#" @click.prevent="handleFooterLink('隐私政策')">隐私政策</a>
            </p>
            <p>技术支持：中国铁道科学研究院集团有限公司</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import {
  SearchOutlined,
  DownOutlined,
  CarOutlined,
  ShoppingOutlined,
  EnvironmentOutlined,
  SwapOutlined,
  CalendarOutlined,
  HistoryOutlined,
  UserOutlined,
  TeamOutlined,
  FileTextOutlined,
  PhoneOutlined,
  QuestionCircleOutlined,
  SafetyCertificateOutlined
} from '@ant-design/icons-vue'

const router = useRouter()

// 搜索关键词
const searchKeyword = ref('')

// 轮播图
const currentSlide = ref(0)
const carouselItems = ref([
  {
    id: 1,
    image: 'https://www.12306.cn/index/images/pic/banner12.jpg',
    title: '铁路出行服务'
  },
  {
    id: 2,
    image: 'https://www.12306.cn/index/images/pic/banner20201223.jpg',
    title: '便民服务'
  },
  {
    id: 3,
    image: 'https://www.12306.cn/index/images/pic/banner20200707.jpg',
    title: '智能出行'
  },
  {
    id: 4,
    image: 'https://www.12306.cn/index/images/pic/banner0619.jpg',
    title: '高铁服务'
  },
  {
    id: 5,
    image: 'https://www.12306.cn/index/images/pic/banner26.jpg',
    title: '客运服务'
  },
  {
    id: 6,
    image: 'https://www.12306.cn/index/images/pic/banner10.jpg',
    title: '铁路资讯'
  }
])

// 搜索标签页
const activeTab = ref('single')
const searchTabs = ref([
  { key: 'single', label: '单程', icon: 'CarOutlined' },
  { key: 'round', label: '往返', icon: 'SwapOutlined' },
  { key: 'transfer', label: '中转换乘', icon: 'NodeIndexOutlined' },
  { key: 'change', label: '退改签', icon: 'EditOutlined' }
])

// 监听标签页切换
const handleTabChange = (tabKey) => {
  activeTab.value = tabKey
  searchForm.searchType = tabKey
}

// 搜索表单
const searchForm = reactive({
  fromStation: '北京',
  toStation: '上海',
  departureDate: dayjs().format('YYYY-MM-DD'),
  returnDate: '',
  isStudent: false,
  isHighSpeed: false,
  searchType: 'single' // single, round, transfer, change
})

// 日期选择器状态
const showDatePicker = ref(false)
const showReturnDatePicker = ref(false)

// 日期选择处理
const handleDateSelect = (date) => {
  searchForm.departureDate = date
  showDatePicker.value = false
}

const handleReturnDateSelect = (date) => {
  searchForm.returnDate = date
  showReturnDatePicker.value = false
}

// 搜索历史
const searchHistory = ref(['北京-上海'])

// 快捷服务
const quickServices = ref([
  { name: '重点旅客预约', icon: 'UserOutlined' },
  { name: '遗失物品查找', icon: 'SearchOutlined' },
  { name: '约车服务', icon: 'CarOutlined' },
  { name: '便民托运', icon: 'ShoppingOutlined' },
  { name: '车站引导', icon: 'EnvironmentOutlined' },
  { name: '站车风采', icon: 'TeamOutlined' },
  { name: '用户反馈', icon: 'FileTextOutlined' },
  { name: '铁路畅行', icon: 'SafetyCertificateOutlined' },
  { name: '候补购票', icon: 'QuestionCircleOutlined' },
  { name: '订单查询', icon: 'FileTextOutlined' },
  { name: '乘客管理', icon: 'TeamOutlined' },
  { name: '个人中心', icon: 'UserOutlined' }
])

// 公告标签页
const activeAnnouncementTab = ref('latest')

// 公告列表
const announcements = ref([
  { id: 1, type: '公 告', title: '关于铁路客运推广使用全面数字化的电子发票的公告', date: '2024-12-11' },
  { id: 2, type: '公 告', title: '关于优化铁路车票改签规则的公告', date: '2024-11-07' },
  { id: 3, type: '公 告', title: '外国护照身份核验使用说明', date: '2024-01-11' },
  { id: 4, type: '公 告', title: '铁路旅客禁止、限制携带和托运物品目录', date: '2023-12-13' },
  { id: 5, type: '公 告', title: '候补购票操作说明', date: '2023-11-30' },
  { id: 6, type: '公 告', title: '关于铁路车站起售时间的公告', date: '2024-04-19' },
  { id: 7, type: '公 告', title: '中国铁路成都局集团有限公司关于2025年11月7日至30日加开部分列车的公告', date: '2022-12-22' },
  { id: 8, type: '公 告', title: '中国铁路成都局集团有限公司关于2025年11月5日至30日加开部分列车的公告', date: '2025-10-15' }
])

// 常见问题列表
const faqList = ref([
  { id: 1, type: '问 答', title: '如何办理铁路畅行会员？', date: '2024-12-10' },
  { id: 2, type: '问 答', title: '候补购票如何操作？', date: '2024-12-08' },
  { id: 3, type: '问 答', title: '学生票如何购买和使用？', date: '2024-12-05' },
  { id: 4, type: '问 答', title: '如何办理退票和改签？', date: '2024-12-03' },
  { id: 5, type: '问 答', title: '身份证丢失如何乘车？', date: '2024-12-01' },
  { id: 6, type: '问 答', title: '儿童票如何购买？', date: '2024-11-28' },
  { id: 7, type: '问 答', title: '如何查询列车正晚点信息？', date: '2024-11-25' },
  { id: 8, type: '问 答', title: '电子客票如何使用？', date: '2024-11-22' }
])

// 信用信息列表
const creditList = ref([
  { id: 1, type: '信 用', title: '铁路旅客信用信息记录管理办法', date: '2024-12-09' },
  { id: 2, type: '信 用', title: '关于在一定期限内适当限制特定严重失信人乘坐火车的意见', date: '2024-12-06' },
  { id: 3, type: '信 用', title: '铁路安全管理条例', date: '2024-12-04' },
  { id: 4, type: '信 用', title: '铁路旅客运输规程', date: '2024-12-02' },
  { id: 5, type: '信 用', title: '关于加强铁路征信体系建设的通知', date: '2024-11-30' },
  { id: 6, type: '信 用', title: '铁路客运服务质量规范', date: '2024-11-27' },
  { id: 7, type: '信 用', title: '关于建立完善守信联合激励和失信联合惩戒制度的指导意见', date: '2024-11-24' },
  { id: 8, type: '信 用', title: '铁路旅客信用信息管理办法实施细则', date: '2024-11-21' }
])

// 计算当前显示的公告列表
const currentAnnouncements = computed(() => {
  switch (activeAnnouncementTab.value) {
    case 'latest':
      return announcements.value
    case 'faq':
      return faqList.value
    case 'credit':
      return creditList.value
    default:
      return announcements.value
  }
})

// 方法
const handleGlobalSearch = () => {
  console.log('全局搜索:', searchKeyword.value)
}

const swapStations = () => {
  const temp = searchForm.value.fromStation
  searchForm.value.fromStation = searchForm.value.toStation
  searchForm.value.toStation = temp
}

const handleTicketSearch = () => {
  // 根据搜索类型进行不同的处理
  switch(searchForm.searchType) {
    case 'single':
      // 单程查询
      router.push({
        name: 'trains',
        query: {
          departure_city: searchForm.fromStation,
          arrival_city: searchForm.toStation,
          travel_date: searchForm.departureDate,
          type: 'single'
        }
      })
      break
    case 'round':
      // 往返查询
      router.push({
        name: 'trains',
        query: {
          departure_city: searchForm.fromStation,
          arrival_city: searchForm.toStation,
          travel_date: searchForm.departureDate,
          return_date: searchForm.returnDate,
          type: 'round'
        }
      })
      break
    case 'transfer':
      // 中转换乘
      console.log('中转换乘功能待实现')
      break
    case 'change':
      // 退改签
      console.log('退改签功能待实现')
      break
    default:
      // 默认单程查询
      router.push({
        name: 'trains',
        query: {
          departure_city: searchForm.fromStation,
          arrival_city: searchForm.toStation,
          travel_date: searchForm.departureDate
        }
      })
  }
  
  // 添加到搜索历史
  const route = `${searchForm.fromStation}-${searchForm.toStation}`
  if (!searchHistory.value.includes(route)) {
    searchHistory.value.unshift(route)
    if (searchHistory.value.length > 3) {
      searchHistory.value.pop()
    }
  }
}

const selectHistoryRoute = (route) => {
  const [from, to] = route.split('-')
  searchForm.value.fromStation = from
  searchForm.value.toStation = to
}

const clearHistory = () => {
  searchHistory.value = []
}

// 顶部导航栏功能
const handleLogin = () => {
  router.push('/login')
}

const handleRegister = () => {
  router.push('/register')
}

const handleMyAccount = () => {
  router.push('/user/profile')
}

const handleOrderInquiry = () => {
  router.push({ name: 'order-inquiry' })
}

const handlePassengerManagement = () => {
  router.push('/user/passengers')
}

const handlePersonalCenter = () => {
  router.push('/user/profile')
}

// 重点旅客预约服务
const handleSpecialPassengerService = () => {
  router.push({ name: 'special-passenger' })
}

// 遗失物品查找
const handleLostItemSearch = () => {
  router.push({ name: 'lost-items' })
}

// 约车服务
const handleCarService = () => {
  router.push({ name: 'car-booking' })
}

// 便民托运
const handleConvenientShipping = () => {
  router.push({ name: 'shipping' })
}

// 车站引导
const handleStationGuide = () => {
  router.push({ name: 'station-guide' })
}

// 站车风采
const handleStationShowcase = () => {
  router.push({ name: 'service-showcase' })
}

// 用户反馈
const handleUserFeedback = () => {
  router.push({ name: 'user-feedback' })
}

// 铁路畅行
const handleRailwayPass = () => {
  router.push({ name: 'railway-pass' })
}

// 候补购票
const handleWaitlistTicket = () => {
  router.push({ name: 'waitlist-ticket' })
}

// 公告点击处理
const handleAnnouncementClick = (announcement) => {
  console.log('点击公告:', announcement.title)
  // 根据公告类型跳转到相应页面
  if (announcement.type === 'announcement') {
    router.push({ name: 'announcement', query: { id: announcement.id } })
  } else if (announcement.type === 'faq') {
    router.push({ name: 'faq', query: { id: announcement.id } })
  } else if (announcement.type === 'credit') {
    router.push({ name: 'credit', query: { id: announcement.id } })
  }
}

// 更多公告处理
const handleMoreAnnouncements = () => {
  // 根据当前激活的标签页跳转到相应页面
  if (activeAnnouncementTab.value === 'latest') {
    router.push({ name: 'announcement' })
  } else if (activeAnnouncementTab.value === 'faq') {
    router.push({ name: 'faq' })
  } else if (activeAnnouncementTab.value === 'credit') {
    router.push({ name: 'credit' })
  }
}

// 页面底部链接处理
const handleFooterLink = (linkName) => {
  console.log('点击底部链接:', linkName)
  // 这里可以根据不同的链接进行相应的跳转或处理
  switch (linkName) {
    case '购票':
      // 滚动到票务搜索区域
      const searchSection = document.querySelector('.search-section')
      if (searchSection) {
        searchSection.scrollIntoView({ behavior: 'smooth' })
      }
      break
    case '订单查询':
      router.push({ name: 'order-inquiry' })
      break
    case '会员服务':
      router.push({ name: 'railway-pass' })
      break
    case '时刻表':
      router.push({ name: 'ticket-schedule' })
      break
    case '候补购票':
      router.push({ name: 'waitlist-ticket' })
      break
    case '重点旅客':
      router.push({ name: 'special-passenger' })
      break
    case '失物招领':
      router.push({ name: 'lost-items' })
      break
    case '约车服务':
      router.push({ name: 'car-booking' })
      break
    case '托运服务':
      router.push({ name: 'shipping' })
      break
    case '车站引导':
      router.push({ name: 'station-guide' })
      break
    case '站车服务':
      router.push({ name: 'service-showcase' })
      break
    case '用户反馈':
      router.push({ name: 'user-feedback' })
      break
    default:
      // 其他链接的处理逻辑
      console.log('暂未实现的链接:', linkName)
      break
  }
}

// 处理快捷服务点击
const handleServiceClick = (serviceName) => {
  switch(serviceName) {
    case '订单查询':
      handleOrderInquiry()
      break
    case '乘客管理':
      handlePassengerManagement()
      break
    case '个人中心':
      handlePersonalCenter()
      break
    case '重点旅客预约':
      handleSpecialPassengerService()
      break
    case '遗失物品查找':
      handleLostItemSearch()
      break
    case '约车服务':
      handleCarService()
      break
    case '便民托运':
      handleConvenientShipping()
      break
    case '车站引导':
      handleStationGuide()
      break
    case '站车风采':
      handleStationShowcase()
      break
    case '用户反馈':
      handleUserFeedback()
      break
    case '铁路畅行':
      handleRailwayPass()
      break
    case '候补购票':
      handleWaitlistTicket()
      break
    default:
      console.log('Service clicked:', serviceName)
  }
}

// 主导航菜单功能
const handleMainNavClick = (navItem) => {
  switch(navItem) {
    case '首页':
      router.push('/')
      break
    case '车票':
      // 滚动到票务查询区域
      const ticketSection = document.querySelector('.ticket-search')
      if (ticketSection) {
        ticketSection.scrollIntoView({ behavior: 'smooth' })
      }
      break
    case '团购服务':
      console.log('团购服务功能待实现')
      break
    case '会员服务':
      console.log('会员服务功能待实现')
      break
    case '站车服务':
      console.log('站车服务功能待实现')
      break
    case '商旅服务':
      console.log('商旅服务功能待实现')
      break
    case '出行指南':
      console.log('出行指南功能待实现')
      break
    case '信息查询':
      handleOrderInquiry()
      break
    default:
      console.log('Navigation clicked:', navItem)
  }
}

onMounted(() => {
  // 设置当前日期
  searchForm.departureDate = dayjs().format('YYYY-MM-DD')
  
  // 启动轮播图自动播放
  startCarouselAutoPlay()
})

// 轮播图自动播放
let carouselTimer = null

const startCarouselAutoPlay = () => {
  carouselTimer = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % carouselItems.value.length
  }, 4000) // 每4秒切换一次
}

const stopCarouselAutoPlay = () => {
  if (carouselTimer) {
    clearInterval(carouselTimer)
    carouselTimer = null
  }
}

// 手动点击指示器时暂停自动播放
const handleIndicatorClick = (index) => {
  currentSlide.value = index
  stopCarouselAutoPlay()
  // 3秒后重新开始自动播放
  setTimeout(() => {
    startCarouselAutoPlay()
  }, 3000)
}
</script>

<style scoped>
/* 12306官网样式复刻 */
.railway-homepage {
  font-family: "Helvetica Neue", Helvetica, Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
  font-size: 14px;
  color: #333;
  background: #fff;
}

/* 头部样式 */
.header {
  background: #fff;
  height: 120px;
  position: relative;
}

.header-container {
  max-width: 1190px;
  margin: 0 auto;
  padding: 0 20px;
}

.header-top {
  display: flex;
  align-items: center;
  height: 80px;
  justify-content: space-between;
}

.logo-section {
  flex-shrink: 0;
}

.logo {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.logo-link {
  color: #0066cc;
  text-decoration: none;
}

.search-section {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}

.search-box {
  position: relative;
  display: flex;
}

.search-input {
  flex: 1;
  height: 36px;
  padding: 0 40px 0 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
}

.top-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  padding: 4px 8px;
}

.nav-link:hover {
  color: #0066cc;
}

.nav-separator {
  color: #ccc;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dropdown-icon {
  font-size: 12px;
}

.auth-links {
  display: flex;
  gap: 8px;
}

/* 主导航 */
.main-nav {
  height: 40px;
  border-top: 1px solid #e5e5e5;
}

.nav-menu {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  height: 100%;
}

.nav-item {
  position: relative;
}

.nav-item .nav-link {
  display: flex;
  align-items: center;
  height: 40px;
  padding: 0 20px;
  color: #333;
  text-decoration: none;
  gap: 4px;
}

.nav-item:hover .nav-link,
.nav-item.active .nav-link {
  background: #f5f5f5;
  color: #0066cc;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: #fff;
  border: 1px solid #e5e5e5;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  min-width: 120px;
  z-index: 1000;
  display: none;
}

.nav-item:hover .dropdown-menu {
  display: block;
}

.dropdown-item {
  display: block;
  padding: 8px 16px;
  color: #333;
  text-decoration: none;
}

.dropdown-item:hover {
  background: #f5f5f5;
  color: #0066cc;
}

/* 主内容区域 */
.main-content {
  max-width: 1190px;
  margin: 0 auto;
  padding: 20px;
}

/* 轮播图和搜索表单合并区域 */
.carousel-search-section {
  margin-bottom: 20px;
}

.carousel-container {
  height: 320px;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  border-radius: 8px;
  position: relative;
  display: flex;
  align-items: stretch;
  overflow: hidden;
}

.carousel-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
  z-index: 1;
}

.carousel-slides {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
}

.carousel-slide.active {
  opacity: 1;
}

.slide-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 102, 204, 0.3) 0%, rgba(0, 68, 153, 0.3) 100%);
}

.carousel-indicators {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  z-index: 3;
}

.indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  cursor: pointer;
}

.indicator.active {
  background: #fff;
  color: #0066cc;
}

/* 内嵌搜索表单 */
.embedded-search-form {
  position: relative;
  z-index: 2;
  width: 50%;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  margin: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  height: 220px;
  overflow: hidden;
}

.search-form-header {
  border-bottom: 1px solid #e5e5e5;
  background: #fff;
  border-radius: 8px 8px 0 0;
}

.search-form-header .service-tabs {
  display: flex;
  border-bottom: none;
}

.search-form-header .tab-item {
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #666;
  font-size: 14px;
}

.search-form-header .tab-item.active {
  color: #0066cc;
  border-bottom: 2px solid #0066cc;
}

.embedded-search-form .search-tabs {
  display: flex;
  gap: 12px;
  padding: 16px 20px 0;
  margin-bottom: 8px;
  border-bottom: 1px solid #e0e0e0;
}

.embedded-search-form .search-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 16px;
  background: #f5f5f5;
  cursor: pointer;
  color: #666;
  font-size: 13px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.embedded-search-form .search-tab.active {
  background: #0066cc;
  color: #fff;
  border-bottom-color: #0066cc;
}

/* 出行类型选项 */
.embedded-search-form .trip-types {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.embedded-search-form .trip-type {
  padding: 4px 8px;
  font-size: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.embedded-search-form .trip-type.active {
  background: #0066cc;
  color: white;
  border-color: #0066cc;
}

.embedded-search-form .search-form {
  background: transparent;
  padding: 16px 20px 20px;
  border-radius: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.embedded-search-form .form-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.embedded-search-form .input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.embedded-search-form .input-label {
  font-size: 11px;
  color: #666;
  margin-bottom: 2px;
}

.embedded-search-form .input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.embedded-search-form .station-input,
.embedded-search-form .date-input {
  width: 100%;
  padding: 6px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 12px;
  background: white;
}

.embedded-search-form .input-icon {
  position: absolute;
  right: 6px;
  width: 14px;
  height: 14px;
  opacity: 0.6;
}

.embedded-search-form .swap-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #f0f0f0;
  border: 1px solid #ddd;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-top: 6px;
  font-size: 12px;
  transition: all 0.3s ease;
}

.embedded-search-form .swap-btn:hover {
  background: #e0e0e0;
}

.embedded-search-form .search-options {
  display: flex;
  gap: 8px;
  align-items: center;
}

.embedded-search-form .option-item {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  font-size: 11px;
  color: #666;
}

.embedded-search-form .search-button {
  height: 32px;
  padding: 0 20px;
  background: linear-gradient(135deg, #0066cc, #004499);
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: bold;
  cursor: pointer;
  letter-spacing: 1px;
  min-width: 70px;
  transition: all 0.3s ease;
}

.embedded-search-form .search-button:hover {
  background: linear-gradient(135deg, #0052a3, #003366);
}

.embedded-search-form .search-button:hover {
  background: #0052a3;
}

.embedded-search-form .search-history {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e5e5e5;
}

.embedded-search-form .history-header {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 12px;
}

.embedded-search-form .history-routes {
  flex: 1;
  margin-left: 12px;
}

.embedded-search-form .history-route {
  color: #0066cc;
  cursor: pointer;
  margin-right: 12px;
  font-size: 12px;
}

.embedded-search-form .clear-history {
  color: #666;
  text-decoration: none;
  font-size: 12px;
}

/* 日期选择器样式 */
.date-picker-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.date-picker {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 400px;
  max-width: 90vw;
}

.date-picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #e5e5e5;
}

.date-picker-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.date-picker-content {
  padding: 20px;
}

.date-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.date-item {
  padding: 12px 8px;
  text-align: center;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.date-item:hover {
  background: #f0f8ff;
  border-color: #1890ff;
}

.date-item.selected {
  background: #1890ff;
  color: white;
  border-color: #1890ff;
}

.date-item .weekday {
  display: block;
  font-size: 12px;
  opacity: 0.7;
  margin-top: 2px;
}

/* 快捷服务 */
.quick-services {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.service-tabs {
  display: flex;
  border-bottom: 1px solid #e5e5e5;
}

.tab-item {
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #666;
}

.tab-item.active {
  color: #0066cc;
  border-bottom: 2px solid #0066cc;
}

/* 响应式设计 - 轮播图和搜索表单 */
@media (max-width: 1024px) {
  .embedded-search-form {
    width: 60%;
  }
}

@media (max-width: 768px) {
  .carousel-container {
    height: 280px;
    flex-direction: column;
  }
  
  .embedded-search-form {
    width: calc(100% - 40px);
    height: auto;
    max-height: calc(100% - 40px);
  }
  
  .carousel-indicators {
    bottom: 10px;
    right: 10px;
  }
}

@media (max-width: 480px) {
  .carousel-container {
    height: 320px;
  }
  
  .embedded-search-form {
    margin: 10px;
    width: calc(100% - 20px);
  }
  
  .embedded-search-form .form-row {
    flex-direction: column;
    gap: 8px;
  }
  
  .embedded-search-form .swap-btn {
    align-self: center;
    margin: 8px 0;
  }
}

/* 快捷服务图标 */
.service-icons {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin: 30px 0;
  padding: 0 20px;
}

.service-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  color: #333;
}

.service-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  background: #f8f9fa;
}

.service-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1890ff, #40a9ff);
  border-radius: 50%;
  margin-bottom: 12px;
  color: white;
  font-size: 24px;
}

.service-name {
  font-size: 14px;
  color: #333;
  text-align: center;
  line-height: 1.4;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .service-icons {
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .service-icons {
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    padding: 0 10px;
  }
  
  .service-item {
    padding: 15px 8px;
  }
  
  .service-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }
  
  .service-name {
    font-size: 12px;
  }
}

/* 公告区域 */
.announcements {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.announcement-tabs {
  display: flex;
  border-bottom: 1px solid #e5e5e5;
}

.announcement-tabs .tab {
  padding: 16px 24px;
  cursor: pointer;
  color: #666;
}

.announcement-tabs .tab.active {
  color: #0066cc;
  border-bottom: 2px solid #0066cc;
}

.announcement-list {
  padding: 20px;
}

.announcement-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.announcement-type {
  color: #0066cc;
  font-weight: bold;
  margin-right: 16px;
  min-width: 60px;
}

.announcement-title {
  flex: 1;
  color: #333;
  text-decoration: none;
  margin-right: 16px;
}

.announcement-title:hover {
  color: #0066cc;
}

.announcement-date {
  color: #999;
  font-size: 12px;
}

.more-link {
  text-align: right;
  margin-top: 16px;
}

.more-link a {
  color: #0066cc;
  text-decoration: none;
}

/* 页面底部 */
.footer {
  background: #2c3e50;
  color: white;
  margin-top: 50px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px 20px;
}

.footer-main {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  margin-bottom: 30px;
}

.footer-section h4 {
  color: #3498db;
  font-size: 16px;
  margin-bottom: 15px;
  font-weight: 600;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-links a {
  color: #bdc3c7;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #3498db;
}

.footer-bottom {
  border-top: 1px solid #34495e;
  padding-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-qr {
  display: flex;
  gap: 30px;
}

.qr-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.qr-code {
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-placeholder {
  color: #2c3e50;
  font-size: 24px;
}

.qr-section span {
  font-size: 12px;
  color: #bdc3c7;
  text-align: center;
}

.footer-info {
  text-align: right;
}

.footer-info p {
  margin: 5px 0;
  font-size: 12px;
  color: #95a5a6;
}

.footer-info a {
  color: #bdc3c7;
  text-decoration: none;
  margin: 0 5px;
}

.footer-info a:hover {
  color: #3498db;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .footer-main {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .footer-main {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .footer-info {
    text-align: center;
  }
  
  .footer-qr {
    justify-content: center;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-top {
    flex-direction: column;
    height: auto;
    padding: 20px 0;
  }
  
  .search-section {
    margin: 20px 0;
    max-width: 100%;
  }
  
  .nav-menu {
    flex-wrap: wrap;
  }
  
  .form-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .service-icons {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .footer-content {
    flex-direction: column;
    gap: 20px;
  }
}
</style>
