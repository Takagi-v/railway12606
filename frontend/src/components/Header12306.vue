<template>
  <!-- 尽量一比一复刻 12306 头部结构与类名 -->
  <div class="header" role="banner">
    <div class="wrapper">
      <div class="header-con">
        <h1 class="logo">
          <!-- 与原站一致：文字隐藏，使用背景图显示 logo -->
          <a href="javascript:;" class="logo-link" aria-label="中国铁路12306">中国铁路12306</a>
        </h1>
        <div class="header-right">
          <!-- 搜索条 -->
          <div class="header-search">
            <div class="search-bd">
              <input type="password" style="display:none" />
              <input
                type="text"
                class="search-input"
                id="search-input"
                aria-label="搜索车票、餐饮、常旅客、相关规章"
                v-model="searchKeyword"
                placeholder="搜索车票、餐饮、常旅客、相关规章"
                aria-haspopup="true"
                @focus="searchActive = true"
                @blur="onSearchBlur"
                @keydown.enter.prevent="handleSearch"
              />
              <!-- 搜索提示 -->
              <div class="search-down" :class="{ show: searchActive }">
                <a href="javascript:;" class="close" @mousedown.prevent="searchActive = false">关闭</a>
                <ul class="search-down-list" role="listbox" aria-expanded="true">
                  <li v-if="!searchKeyword">输入关键词以获取建议</li>
                  <li v-else-if="filteredSuggestions.length === 0">无匹配项</li>
                  <li v-for="(s, i) in filteredSuggestions" :key="i" @mousedown.prevent="applySuggestion(s)">{{ s }}</li>
                </ul>
              </div>
              <!-- 搜索历史 -->
              <div class="search-history" :class="{ show: searchActive }">
                <a href="javascript:;" class="history-clear" @mousedown.prevent="clearHistory">清除</a>
                <h3 class="search-history-tit">搜索历史</h3>
                <ul class="search-history-list" role="listbox" aria-expanded="true">
                  <li v-for="(s, i) in searchHistory" :key="i" @mousedown.prevent="applyHistory(s)">{{ s }}</li>
                </ul>
              </div>
            </div>
            <a class="search-btn" href="javascript:;" aria-label="点击搜索" @mousedown.prevent="handleSearch">
              <i class="hdr-icon hdr-search"></i>
            </a>
          </div>
          <!-- 右侧顶部菜单：无障碍 敬老版 English 我的12306 登录/注册 -->
          <ul class="header-menu" role="menubar" id="topMenu">
            <li class="menu-item">
              <a href="javascript:;" class="menu-nav-hd">无障碍</a>
            </li>
            <li class="menu-item menu-line">|</li>
            <li class="menu-item">
              <a href="javascript:;" class="menu-nav-hd">敬老版</a>
            </li>
            <li class="menu-item menu-line">|</li>
            <li class="menu-item menu-nav" role="menuitem">
              <a href="https://www.12306.cn/en/index.html" class="menu-nav-hd item" title="English">
                English <i class="caret"></i>
              </a>
              <ul class="menu-nav-bd" role="menu">
                <li><a href="javascript:;" title="简体中文">简体中文</a></li>
                <li><a href="https://www.12306.cn/en/index.html" title="English">English</a></li>
              </ul>
            </li>
            <li class="menu-item menu-line">|</li>
            <li class="menu-item menu-nav" role="menuitem">
              <a href="javascript:;" class="menu-nav-hd item" id="my12306" @click.prevent="goMy12306">
                我的12306 <i class="caret"></i>
              </a>
              <ul class="menu-nav-bd" role="menu">
                <li><a href="javascript:;" @click.prevent="goOrderInquiry">火车票订单</a></li>
                <li><a href="javascript:;">候补订单</a></li>
                <li><a href="javascript:;">计次•定期票订单</a></li>
                <li><a href="javascript:;">约号订单</a></li>
                <li><a href="javascript:;">电子发票</a></li>
                <li><a href="javascript:;">本人车票</a></li>
                <li class="nav-line"></li>
                <li><a href="javascript:;">我的餐饮•特产</a></li>
                <li><a href="javascript:;">我的保险</a></li>
                <li><a href="javascript:;">我的会员</a></li>
                <li class="nav-line"></li>
                <li><a href="javascript:;">查看个人信息</a></li>
                <li><a href="javascript:;">账户安全</a></li>
                <li class="nav-line"></li>
                <li><a href="javascript:;" @click.prevent="goPassengers">乘车人</a></li>
                <li><a href="javascript:;">地址管理</a></li>
                <li class="nav-line"></li>
                <li><a href="javascript:;">温馨服务查询</a></li>
              </ul>
            </li>
            <li class="menu-item menu-line">|</li>
            <li class="menu-item menu-login" role="menuitem">
              <a href="javascript:;" @click.prevent="handleLogin">登录</a>
              <a href="javascript:;" class="ml" @click.prevent="handleRegister">注册</a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 次级导航条（蓝色） -->
    <div class="nav-box" role="navigation">
      <ul class="nav" role="menubar" id="member">
        <!-- 首页 -->
        <li role="menuitem" id="J-index" class="nav-item nav-item-w1 active">
          <a href="javascript:;" class="nav-hd" @click.prevent="goHome">首页</a>
        </li>
        <!-- 车票 -->
        <li role="menuitem" id="J-chepiao" class="nav-item nav-item-w1">
          <a href="javascript:void(0)" class="nav-hd item">
            车票 <i class="hdr-icon hdr-down"></i>
          </a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col2">
                <h3 class="nav-tit">购买</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <!-- 按官网行序：单程、往返 | 中转换乘、计次•定期票 -->
                  <li class="nav_dan"><a href="javascript:;" @click.prevent="openTicket('dc')">单程</a></li>
                  <li class="nav_wang"><a href="javascript:;" @click.prevent="openTicket('wf')">往返</a></li>
                  <li><a href="javascript:;" @click.prevent="openTransfer">中转换乘</a></li>
                  <li><a href="javascript:;" @click.prevent="openSeason">计次•定期票</a></li>
                </ul>
              </div>
              <div class="nav-bd-item nav-col2">
                <h3 class="nav-tit">变更</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <!-- 按官网行序：退票、改签 | 变更到站 -->
                  <li class="nav_ref item"><a href="javascript:;">退票</a></li>
                  <li class="nav_res item"><a href="javascript:;">改签</a></li>
                  <li class="nav_chg item"><a href="javascript:;">变更到站</a></li>
                </ul>
              </div>
              <div class="nav-bd-item nav-col2 border-none">
                <h3 class="nav-tit">更多</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">中铁银通卡</a></li>
                  <li><a href="javascript:;">国际列车</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
        <!-- 团购服务 -->
        <li role="menuitem" id="J-tuangoufuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item">团购服务 <i class="hdr-icon hdr-down"></i></a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col6 border-none">
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">务工人员</a></li>
                  <li><a href="javascript:;">学生团体</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
        <!-- 会员服务 -->
        <li role="menuitem" id="J-huiyuanfuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item">会员服务 <i class="hdr-icon hdr-down"></i></a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col6 border-none">
                <ul class="nav-con nav-simple" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">会员管理</a></li>
                  <li><a href="javascript:;">积分账户</a></li>
                  <li><a href="javascript:;">积分兑换</a></li>
                  <li><a href="javascript:;">会员专享</a></li>
                  <li class="item"><a href="javascript:;">会员中心</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
        <!-- 站车服务 -->
        <li role="menuitem" id="J-zhanchefuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item">站车服务 <i class="hdr-icon hdr-down"></i></a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col4 border-none">
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">特殊重点旅客</a></li>
                  <li><a href="javascript:;">便民托运</a></li>
                  <li><a href="javascript:;">约车服务</a></li>
                  <li><a href="javascript:;">车站引导</a></li>
                  <li><a href="javascript:;">遗失物品查找</a></li>
                  <li><a href="javascript:;">动车组介绍</a></li>
                  <li><a href="javascript:;">定制接送</a></li>
                  <li><a href="javascript:;">站车风采</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
        <!-- 商旅服务 -->
        <li role="menuitem" id="J-shanlvfuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item">商旅服务 <i class="hdr-icon hdr-down"></i></a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col6 border-none">
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">餐饮•特产</a></li>
                  <li><a href="javascript:;">保险</a></li>
                  <li><a href="javascript:;">雪具快运</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
        <!-- 出行指南 -->
        <li role="menuitem" id="J-chuxingzhinan" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item">出行指南 <i class="hdr-icon hdr-down"></i></a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col2">
                <h3 class="nav-tit">常见问题</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">车票</a></li>
                  <li><a href="javascript:;">购票</a></li>
                  <li><a href="javascript:;">改签</a></li>
                  <li><a href="javascript:;">退票</a></li>
                  <li><a href="javascript:;">更多&gt;&gt;</a></li>
                </ul>
              </div>
              <div class="nav-bd-item nav-col2">
                <h3 class="nav-tit">旅客须知</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">身份核验</a></li>
                  <li><a href="javascript:;">更多&gt;&gt;</a></li>
                </ul>
              </div>
              <div class="nav-bd-item nav-col2 border-none">
                <h3 class="nav-tit">相关章程</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">铁路旅客运输规程</a></li>
                  <li><a href="javascript:;">广深港高速铁路跨境旅客运输组织规则</a></li>
                  <li><a href="javascript:;">铁路旅客禁止、限制携带和托运物品目录</a></li>
                  <li><a href="javascript:;">更多&gt;&gt;</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
        <!-- 信息查询 -->
        <li role="menuitem" id="J-xinxichaxun" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item">信息查询 <i class="hdr-icon hdr-down"></i></a>
          <div class="nav-bd">
            <div class="wrapper nav-row">
              <div class="nav-bd-item nav-col4">
                <h3 class="nav-tit">常用查询</h3>
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">正晚点</a></li>
                  <li><a href="javascript:;" @click.prevent="goSchedule">时刻表</a></li>
                  <li><a href="javascript:;">公布票价</a></li>
                  <li><a href="javascript:;">检票口</a></li>
                  <li><a href="javascript:;">起售时间</a></li>
                  <li><a href="javascript:;">天气</a></li>
                  <li><a href="javascript:;">交通查询</a></li>
                  <li><a href="javascript:;">代售点</a></li>
                  <li><a href="javascript:;">客服电话</a></li>
                  <li><a href="javascript:;">列车状态</a></li>
                </ul>
              </div>
              <div class="nav-bd-item nav-col2 border-none">
                <ul class="nav-con nav-two" role="menu" aria-hidden="true">
                  <li><a href="javascript:;">最新发布</a></li>
                  <li><a href="javascript:;">信用信息</a></li>
                </ul>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchKeyword = ref('')
const searchActive = ref(false)
const searchHistory = ref<string[]>(['动车组介绍', '正晚点查询', '代售点'])
const suggestions = ref<string[]>(['购票', '改签', '退票', '起售时间'])
const filteredSuggestions = computed(() => {
  const kw = searchKeyword.value.trim()
  if (!kw) return suggestions.value
  return suggestions.value.filter(s => s.includes(kw))
})

const onSearchBlur = () => {
  // 延迟关闭，保证选择项点击可用
  setTimeout(() => (searchActive.value = false), 120)
}
const handleSearch = () => {
  const kw = searchKeyword.value.trim()
  if (!kw) return
  searchHistory.value.unshift(kw)
}
const applyHistory = (kw: string) => {
  searchKeyword.value = kw
  handleSearch()
}
const applySuggestion = (kw: string) => {
  searchKeyword.value = kw
  handleSearch()
}
const clearHistory = () => {
  searchHistory.value = []
}

// 路由/交互占位：保持与原站头部一致的行为表象
const goHome = () => {
  router.push({ path: '/' })
}
const openTicket = (type: 'dc' | 'wf') => {
  const q = type === 'dc' ? { type: 'single' } : { type: 'round' }
  router.push({ path: '/trains', query: q })
}
const openTransfer = () => {
  router.push({ path: '/trains', query: { transfer: 'true' } })
}
const openSeason = () => {
  router.push({ path: '/season-tickets' })
}
const goSchedule = () => {
  router.push({ name: 'ticket-schedule' })
}

// 路由跳转：登录/注册与我的12306
const handleLogin = () => router.push('/login')
const handleRegister = () => router.push('/register')
const goMy12306 = () => router.push('/user/profile')
const goOrderInquiry = () => router.push({ name: 'order-inquiry' })
const goPassengers = () => router.push('/user/passengers')

// 远程 logo 加载失败回退到本地 /pics/logo@2x.png
const tryLoadImage = (url: string) => new Promise<void>((resolve, reject) => {
  const img = new Image()
  img.onload = () => resolve()
  img.onerror = () => reject()
  img.src = url
})

onMounted(() => {
  tryLoadImage('https://www.12306.cn/index/images/logo@2x.png').catch(() => {
    document.documentElement.style.setProperty(
      '--logo-img',
      'image-set(url("/pics/logo@2x.png") 2x, url("/pics/logo@2x.png") 1x)'
    )
  })
})
</script>

<style scoped>
/* 容器与栅格 */
.wrapper { width: 1200px; margin: 0 auto; }
.header { background: #fff; }
.header-con { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; }
.logo { margin: 0; }
.logo .logo-link {
  display: block;
  width: 200px; height: 50px;
  text-indent: -9999px; /* 隐藏文字 */
  /* 远程 image-set 背景图，支持 1x/2x；提供本地回退变量 */
  background-image: var(--logo-img, image-set(url('https://www.12306.cn/index/images/logo.png') 1x, url('https://www.12306.cn/index/images/logo@2x.png') 2x));
  background-repeat: no-repeat;
  background-position: left center;
  background-size: contain;
}

.header-right { display: flex; align-items: center; }
.header-search { width: 380px; display: flex; align-items: center; }
.search-bd { position: relative; width: 350px; }
.search-input { width: 100%; height: 34px; line-height: 34px; padding: 0 10px; border: 1px solid #dedede; outline: none; }
.search-btn { height: 34px; line-height: 34px; padding: 0 10px; background: #3b99fc; color: #fff; display: inline-block; }
.hdr-icon { display: inline-block; }
.hdr-search { width: 16px; height: 16px; background: url('data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\"><path fill=\"white\" d=\"M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 5 1.5-1.5-5-5zm-6 0C8.01 14 6 11.99 6 9.5S8.01 5 10.5 5 15 7.01 15 9.5 12.99 14 10.5 14z\"/></svg>') center/contain no-repeat; }

/* 搜索下拉 */
.search-down, .search-history { display: none; position: absolute; left: 0; right: 0; background: #fff; border: 1px solid #dedede; z-index: 10; }
.search-down { top: 36px; }
.search-history { top: 36px; margin-top: 8px; }
.search-down.show, .search-history.show { display: block; }
.search-down .close { position: absolute; right: 8px; top: 6px; color: #999; }
.search-history-tit { font-weight: 600; padding: 8px; margin: 0; }
.search-down-list, .search-history-list { list-style: none; padding: 8px; }
.search-down-list li, .search-history-list li { padding: 6px 8px; cursor: pointer; }
.search-down-list li:hover, .search-history-list li:hover { background: #f5f5f5; }
.history-clear { position: absolute; right: 8px; top: 8px; color: #999; }

/* 顶部菜单（对齐 12306，更轻量紧凑） */
.header-menu { height: 40px; line-height: 40px; display: flex; align-items: center; flex-wrap: nowrap; gap: 0; margin: 0 0 0 20px; list-style: none; padding: 0; font-size: 14px; }
.menu-item { height: 40px; color: #333; display: flex; align-items: center; padding: 0 6px; }
.menu-line { color: #999; padding: 0 4px; }
.menu-nav { position: relative; }
.menu-nav-hd { color: #333; }
.menu-nav .caret { display: inline-block; width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 6px solid #b3b3b3; margin-left: 4px; vertical-align: middle; }
/* 顶部菜单链接不换行、统一行高（仅作用于顶层菜单项） */
.header-menu > .menu-item > a { display: inline-block; white-space: nowrap; line-height: 40px; }
.menu-login { display: flex; align-items: center; }
/* 下拉面板：窄边框、微阴影、紧凑内边距 */
.menu-nav-bd { display: none; position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid #ddd; min-width: 180px; padding: 4px 0; z-index: 20; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.menu-nav:hover .menu-nav-bd { display: block; }
.menu-nav-bd li a { display: block; padding: 0 12px; white-space: nowrap; color: #333; font-size: 12px; line-height: 26px; }
.menu-nav-bd li a:hover { background: #f5f5f5; }
.menu-login a { color: #333; }
.menu-login a.ml { margin-left: 8px; }
.nav-line { height: 1px; margin: 4px 0; background: #eee; }

/* 次级导航条 */
.nav-box { background: #3b99fc; height: 40px; position: relative; display: flex; justify-content: center; margin-left: calc((100vw - 100%) / 2); margin-right: calc((100vw - 100%) / 2); }
.nav { width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; padding: 0; list-style: none; box-sizing: border-box; }
.nav-item { display: block; }
.nav-hd { display: block; color: #fff; height: 40px; line-height: 40px; padding: 0 16px; }
.nav-item.active .nav-hd { font-weight: 600; }
.hdr-down { width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 7px solid #fff; margin-left: 6px; }
.nav-bd { display: none; position: absolute; top: 40px; left: 0; right: 0; background: #fff; border-bottom: 1px solid #dedede; padding: 16px 0; z-index: 30; overflow: hidden; }
.nav-item:hover .nav-bd { display: block; }
.nav-bd .wrapper { width: 1200px; margin: 0 auto; display: flex; gap: 24px; align-items: flex-start; }
.nav-bd-item { float: none; min-width: 220px; padding: 0; border-right: 1px solid #eaeaea; overflow: hidden; }
.nav-bd-item.border-none { border-right: none; }
.nav-col2 { width: 384px; flex: 0 0 384px; }
.nav-col4 { width: 420px; flex: 0 0 420px; }
.nav-col6 { width: 600px; flex: 0 0 600px; }
.nav-tit { font-weight: 600; color: #3b99fc; margin-bottom: 12px; }
.nav-con { list-style: none; }
.nav-con li { line-height: 32px; }
.nav-con li a { color: #333; }
.nav-con li a:hover { color: #3b99fc; }

/* 无大类横向列举（会员服务等）：按官网为右分隔线，末项无线 */
#J-huiyuanfuwu .nav-con.nav-simple { display: flex; align-items: center; justify-content: flex-start; gap: 24px; padding: 8px 0; }
#J-huiyuanfuwu .nav-con.nav-simple li { font-size: 16px; font-weight: 500; color: #333; border-left: none; padding-left: 0; }
#J-huiyuanfuwu .nav-con.nav-simple li:not(:last-child) { border-right: 1px solid #acd1f9; padding-right: 32px; }
#J-huiyuanfuwu .nav-con.nav-simple li:last-child { border-right: none; padding-right: 0; }

/* 通用：两列按行填充，与官网分栏一致 */
.nav-con.nav-two {
  display: grid;
  grid-auto-flow: row;               /* 先填充一行中的两列，再开新行 */
  grid-template-columns: 198px 198px;/* 两列固定宽度 */
  grid-auto-rows: 32px;              /* 每行固定高度，保证对齐 */
  column-gap: 48px;
  row-gap: 6px;
  align-content: start;
  align-items: start;
  justify-items: start;
}
/* 移除可能由外部样式注入的清浮动伪元素，避免参与网格布局 */
.nav-con.nav-two::before,
.nav-con.nav-two::after {
  content: none !important;
  display: none !important;
}
/* 在 420px 容器（nav-col4、nav-col2）里使用两列并缩小间距以贴合 */
.nav-bd-item.nav-col4 .nav-con.nav-two,
.nav-bd-item.nav-col2 .nav-con.nav-two {
  grid-auto-flow: row;
  grid-template-columns: 1fr 1fr; /* 自适应容器宽度，避免溢出 */
  column-gap: 24px;
}
/* 出行指南-常见问题包含5项，需要每列允许3行以避免多开列 */
#J-chuxingzhinan .nav-bd-item:first-child .nav-con.nav-two { grid-template-rows: repeat(3, auto); }
/* 车票栏目：每列内容从顶部起始，使用单列竖排避免对齐偏差 */
#J-chepiao .nav-con.nav-two {
  /* 改为按行填充，两列固定宽度，严格对齐 */
  display: grid;
  grid-auto-flow: row;               /* 先填充行，再到下一行 */
  grid-template-columns: 198px 198px;/* 两列固定宽度，与官网一致 */
  grid-template-rows: 32px 32px;     /* 两行固定高度，保证齐平 */
  column-gap: 24px;
  row-gap: 6px;
  align-content: start;
  align-items: start;
  justify-items: start;
}
/* 车票-更多：仅一行两列 */
#J-chepiao .nav-bd-item:last-child .nav-con.nav-two {
  grid-template-rows: repeat(1, auto);
}
/* 站车服务：8 项按 4 列 × 2 行分布，避免只占两列显空 */
#J-zhanchefuwu .nav-bd-item.nav-col4 { width: 864px; flex: 0 0 864px; }
#J-zhanchefuwu .nav-con.nav-two {
  grid-auto-flow: row;
  grid-template-columns: 198px 198px 198px 198px; /* 四列 */
  grid-template-rows: 32px 32px;                 /* 两行 */
  column-gap: 24px;
}
/* 商旅服务：三项并排一行显示 */
#J-shanlvfuwu .nav-con.nav-two {
  grid-auto-flow: row;
  grid-template-columns: 198px 198px 198px; /* 三列 */
  grid-auto-rows: 32px;
  column-gap: 24px;
}
/* 信息查询：常用查询 五列 × 两行，右侧两项一列 */
#J-xinxichaxun .nav-bd-item.nav-col4 { width: 990px; flex: 0 0 990px; }
#J-xinxichaxun .nav-bd-item.nav-col4 .nav-con.nav-two {
  grid-auto-flow: row;
  grid-template-columns: 198px 198px 198px 198px 198px; /* 五列 */
  grid-template-rows: 32px 32px;                          /* 两行 */
  column-gap: 0;                                          /* 官方为并排分隔线效果，这里不留列间距 */
}
#J-xinxichaxun .nav-bd-item.nav-col2 { width: 198px; flex: 0 0 198px; }
#J-xinxichaxun .nav-bd-item.nav-col2 { min-width: 198px; }
#J-xinxichaxun .nav-bd-item.nav-col2 { padding-top: 36px; }
#J-xinxichaxun .nav-bd-item.nav-col2 .nav-con.nav-two {
  grid-auto-flow: row;
  grid-template-columns: 198px;                           /* 单列 */
  grid-auto-rows: 32px;
  column-gap: 0;
}
/* 导航条占满整行 */
.nav-box { width: 100%; }

/* 防止外部（SectionFirst 引入的）官网全局 CSS 与 iconfont 干扰头部
   现象：菜单项前出现方框乱码，多数由 ::before/::after 注入的私有区字符引起
   处理：在本组件作用域内，移除伪元素内容，并禁用 iconfont 类名 */
.nav-hd::before,
.nav-hd::after,
.nav-item::before,
.nav-item::after {
  content: none !important;
}
.nav-hd,
.nav-item,
.nav-con li a {
  font-family: inherit !important;
}
.iconfont,
.global-iconfont {
  display: none !important;
}
</style>
<style scoped>
.item::before,
.item::after {
  content: none !important;
}
</style>