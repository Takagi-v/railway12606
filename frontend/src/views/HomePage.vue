<template>
  <div class="railway-homepage">
    <!-- 顶部导航栏（组件化） -->
    <Header12306 />

    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 复刻 12306 .section-first 查询与轮播组件 -->
      <SectionFirst12306 />

      <!-- 服务列表（与官网一致） -->
      <ServiceList12306 />

      <!-- 服务大图（service-lg 复刻） -->
      <ServiceLg12306 />
      <!-- 新闻公告（newstab 复刻） -->
      <NewsTab12306 />
    </main>

    <LoginFooter />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import Header12306 from '../components/Header12306.vue'
import LoginFooter from '../components/LoginFooter.vue'
import SectionFirst12306 from '../components/SectionFirst12306.vue'
import ServiceList12306 from '../components/ServiceList12306.vue'
import ServiceLg12306 from '../components/ServiceLg12306.vue'
import NewsTab12306 from '../components/NewsTab12306.vue'
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
const handleTabChange = tabKey => {
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
const handleDateSelect = date => {
  searchForm.departureDate = date
  showDatePicker.value = false
}

const handleReturnDateSelect = date => {
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

// 方法
const handleGlobalSearch = () => {
  console.log('全局搜索:', searchKeyword.value)
}

const swapStations = () => {
  const temp = searchForm.fromStation
  searchForm.fromStation = searchForm.toStation
  searchForm.toStation = temp
}

const pushToTicketPage = (name, extraQuery = {}) => {
  router.push({
    name,
    query: {
      departure_city: searchForm.fromStation,
      arrival_city: searchForm.toStation,
      travel_date: searchForm.departureDate,
      ...extraQuery
    }
  })
}

const handleTicketSearch = () => {
  // 根据搜索类型进行不同的处理
  switch (searchForm.searchType) {
    case 'single':
      pushToTicketPage('leftTicket-single', { type: 'single' })
      break
    case 'round':
      pushToTicketPage('leftTicket-round', {
        type: 'round',
        return_date:
          searchForm.returnDate ||
          dayjs(searchForm.departureDate).add(1, 'day').format('YYYY-MM-DD')
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
      pushToTicketPage('leftTicket-single')
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

const selectHistoryRoute = route => {
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
  router.push({ path: '/user/profile', query: { group: '个人中心' } })
}

const handleOrderInquiry = () => {
  router.push({ name: 'order-inquiry' })
}

const handlePassengerManagement = () => {
  router.push('/user/passengers')
}

const handlePersonalCenter = () => {
  router.push({ path: '/user/profile', query: { group: '个人中心' } })
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

// 页面底部链接处理
const handleFooterLink = linkName => {
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
const handleServiceClick = serviceName => {
  switch (serviceName) {
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
const handleMainNavClick = navItem => {
  switch (navItem) {
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
const handleIndicatorClick = index => {
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
  font-family:
    'Helvetica Neue', Helvetica, Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei',
    'WenQuanYi Micro Hei', sans-serif;
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  background: rgba(255, 255, 255, 0.5);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
