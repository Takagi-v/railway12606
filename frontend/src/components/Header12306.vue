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
              <input type="password" style="display: none" />
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
                <a href="javascript:;" class="close" @mousedown.prevent="searchActive = false">
                  关闭
                </a>
                <ul class="search-down-list" role="listbox" aria-expanded="true">
                  <li v-if="!searchKeyword">输入关键词以获取建议</li>
                  <li v-else-if="filteredSuggestions.length === 0">无匹配项</li>
                  <li
                    v-for="(s, i) in filteredSuggestions"
                    :key="i"
                    @mousedown.prevent="applySuggestion(s)"
                  >
                    {{ s }}
                  </li>
                </ul>
              </div>
              <!-- 搜索历史 -->
              <div class="search-history" :class="{ show: searchActive }">
                <a href="javascript:;" class="history-clear" @mousedown.prevent="clearHistory">
                  清除
                </a>
                <h3 class="search-history-tit">搜索历史</h3>
                <ul class="search-history-list" role="listbox" aria-expanded="true">
                  <li v-for="(s, i) in searchHistory" :key="i" @mousedown.prevent="applyHistory(s)">
                    {{ s }}
                  </li>
                </ul>
              </div>
            </div>
            <a
              class="search-btn"
              href="javascript:;"
              aria-label="点击搜索"
              @mousedown.prevent="handleSearch"
            >
              <i class="icon icon-search"></i>
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
                English
                <i class="caret"></i>
              </a>
              <ul class="menu-nav-bd" role="menu">
                <li><a href="javascript:;" title="简体中文">简体中文</a></li>
                <li><a href="https://www.12306.cn/en/index.html" title="English">English</a></li>
              </ul>
            </li>
            <li class="menu-item menu-line">|</li>
            <li
              class="menu-item menu-nav"
              role="menuitem"
              @mouseenter="showMy12306"
              @mouseleave="hideMy12306"
            >
              <a
                href="javascript:;"
                class="menu-nav-hd item"
                id="my12306"
                @click.prevent="goMy12306"
              >
                我的12306
                <i class="caret"></i>
              </a>
              <ul class="menu-nav-bd" role="menu" :class="{ show: my12306Active }">
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
            <li class="menu-item menu-login" role="menuitem" v-if="!isAuthenticated">
              <a href="javascript:;" @click.prevent="handleLogin">登录</a>
              <a href="javascript:;" class="ml" @click.prevent="handleRegister">注册</a>
            </li>
            <li role="menuitem" id="J-header-logout" class="menu-item menu-login" v-else>
              <span class="greeting">您好，</span>
              <a id="login_user" href="javascript:;" class="colorA" @click.prevent="goProfile">
                <span class="user-name">{{ displayName }}</span>
              </a>
              <span class="sep">|</span>
              <a href="javascript:;" @click.prevent="handleLogout">退出</a>
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
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-3">
            车票
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" id="megamenu-3">
            <div class="nav-bd-item nav-col2">
              <h3 class="nav-tit">购买</h3>
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li class="nav_dan" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="leftTicket/init?linktypeid=dc" data-redirect="Y" href="javascript:;" @click.prevent="openTicket('dc')">单程</a>
                </li>
                <li class="nav_wang" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="leftTicket/init?linktypeid=wf" data-redirect="Y" href="javascript:;" @click.prevent="openTicket('wf')">往返</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="lcQuery/init" data-redirect="Y" href="javascript:;" @click.prevent="openTransfer">中转换乘</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/commutation_index.html" data-redirect="Y" href="javascript:;" @click.prevent="openSeason">计次•定期票</a>
                </li>
              </ul>
            </div>
            <div class="nav-bd-item nav-col2">
              <h3 class="nav-tit">变更</h3>
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li class="nav_ref item" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/train_order.html?type=2&amp;typefilt=4" data-redirect="Y" href="javascript:;">退票</a>
                </li>
                <li class="nav_res item" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/train_order.html?type=2&amp;typefilt=2" data-redirect="Y" href="javascript:;">改签</a>
                </li>
                <li class="nav_chg item" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/train_order.html?type=2&amp;typefilt=3" data-redirect="Y" href="javascript:;">变更到站</a>
                </li>
                <li></li>
              </ul>
            </div>
            <div class="nav-bd-item nav-col2">
              <h3 class="nav-tit border-none">更多</h3>
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/ticket/zt_card.html" data-redirect="Y" href="javascript:;">中铁银通卡</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/ticket/international_train.html" data-redirect="Y" href="javascript:;">国际列车</a>
                </li>
              </ul>
            </div>
          </div>
        </li>
        <!-- 团购服务 -->
        <li role="menuitem" id="J-tuangoufuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-4">
            团购服务
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" id="megamenu-4">
            <div class="nav-bd-item nav-col6">
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/group/group_management.html?type=1" data-redirect="Y" href="javascript:;">务工人员</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/group/group_management.html?type=2" data-redirect="Y" href="javascript:;">学生团体</a>
                </li>
              </ul>
            </div>
          </div>
        </li>
        <!-- 会员服务 -->
        <li role="menuitem" id="J-huiyuanfuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-5">
            会员服务
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" id="megamenu-5">
            <div class="nav-bd-item nav-col6">
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">会员管理</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">积分账户</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">积分兑换</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="3" data-href="index.html" data-redirect="Y" href="javascript:;">会员专享</a>
                </li>
                <li class="border-none item" role="menuitemradio">
                  <a name="g_href" data-type="3" data-href="welcome.html" data-redirect="Y" href="javascript:;">会员中心</a>
                </li>
              </ul>
            </div>
          </div>
        </li>
        <!-- 站车服务 -->
        <li role="menuitem" id="J-zhanchefuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-6">
            站车服务
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" id="megamenu-6">
            <div class="nav-bd-item nav-col4">
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/icentre_qxyyInfo.html" data-redirect="Y" href="javascript:;">特殊重点旅客</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/station/hand.html" data-redirect="Y" href="javascript:;">便民托运</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/station/shared_Car.html" data-redirect="Y" href="javascript:;">约车服务</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="4" data-href="czyd_2143/" data-redirect="Y" href="javascript:;">车站引导</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/icentre_lostInfo.html" data-redirect="Y" href="javascript:;">遗失物品查找</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/station/train_intro.html" data-redirect="Y" href="javascript:;">动车组介绍</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="4" data-href="zcfc_2548/" data-redirect="Y" href="javascript:;">站车风采</a>
                </li>
              </ul>
            </div>
          </div>
        </li>
        <!-- 商旅服务 -->
        <li role="menuitem" id="J-shanlvfuwu" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-7">
            商旅服务
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" id="megamenu-7">
            <div class="nav-bd-item nav-col6">
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="10" data-href="index.html" data-redirect="Y" href="javascript:;">餐饮•特产</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/my_insurance.html" data-redirect="Y" href="javascript:;">保险</a>
                </li>
                <li class="border-none" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/snow_checkedBaggage.html" data-redirect="Y" href="javascript:;">雪具快运</a>
                </li>
              </ul>
            </div>
          </div>
        </li>
        <!-- 出行指南 -->
        <li role="menuitem" id="J-chuxingzhinan" class="nav-item">
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-8">
            出行指南
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" aria-hidden="true" id="megamenu-8">
            <div class="nav-bd-item nav-col2">
              <h3 class="nav-tit">常见问题</h3>
              <ul class="nav-con" role="menu">
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/ticketType.html" data-redirect="Y" href="javascript:;">车票</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/ticketWindow.html" data-redirect="Y" href="javascript:;">购票</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/windowEndorse.html" data-redirect="Y" href="javascript:;">改签</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/windowRefund.html" data-redirect="Y" href="javascript:;">退票</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/help.html" data-redirect="Y" href="javascript:;" class="txt-lighter" title="常见问题">更多&gt;&gt;</a>
                </li>
                <li></li>
              </ul>
            </div>
            <div class="nav-bd-item nav-col2">
              <h3 class="nav-tit">旅客须知</h3>
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means5" data-redirect="Y" href="javascript:;">身份核验</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/help.html" data-redirect="Y" href="javascript:;" class="txt-lighter">更多&gt;&gt;</a>
                </li>
                <li></li>
              </ul>
            </div>
            <div class="nav-bd-item nav-col2">
              <h3 class="nav-tit border-none">相关章程</h3>
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means2" data-redirect="Y" href="javascript:;">铁路旅客运输规程</a>
                </li>
                <li class="border-none item" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means7" data-redirect="Y" href="javascript:;">广深港高速铁路跨境旅客运输组织规则</a>
                </li>
                <li style="text-overflow: ellipsis; white-space: nowrap" role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/saleTicketMeans.html?linktypeid=means6" data-redirect="Y" href="javascript:;">铁路旅客禁止、限制携带和托运物品目录</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="gonggao/help.html" data-redirect="Y" href="javascript:;" class="txt-lighter">更多&gt;&gt;</a>
                </li>
                <li></li>
              </ul>
            </div>
          </div>
        </li>
        <!-- 信息查询 -->
        <li role="menuitem" id="J-xinxichaxun" class="nav-item last">
          <a href="javascript:void(0)" class="nav-hd item" aria-expanded="true" aria-haspopup="true" aria-controls="megamenu-9">
            信息查询
            <i class="icon icon-down"></i>
          </a>
          <div class="nav-bd" id="megamenu-9">
            <div class="nav-bd-item nav-col5">
              <h3 class="nav-tit border-none">常用查询</h3>
              <ul class="nav-con" role="menu" aria-hidden="true">
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/onTimeOrLate.html" data-redirect="Y" href="javascript:;">正晚点</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="queryTrainInfo/init" data-redirect="Y" href="javascript:;" @click.prevent="goSchedule">时刻表</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="view/queryPublicIndex.html" data-redirect="Y" href="javascript:;">公布票价</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/infos/ticket_check.html" data-redirect="Y" href="javascript:;">检票口</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/infos/sale_time.html" data-redirect="Y" href="javascript:;">起售时间</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-href="https://12306.weather.com.cn/pc.html" data-redirect="N" href="javascript:;" data-target="_blank">天气</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/infos/jiaotong.html" data-redirect="Y" href="javascript:;">交通查询</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="2" data-href="queryAgencySellTicket/init" data-redirect="Y" href="javascript:;">代售点</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/infos/service_number.html" data-redirect="Y" href="javascript:;">客服电话</a>
                </li>
                <li role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="view/infos/train-query-status.html" data-redirect="Y" href="javascript:;">列车状态
                  </a>
                </li>
              </ul>
            </div>
            <div class="nav-bd-item">
              <ul class="nav-con nav-con-pt" role="menu" aria-hidden="true">
                <li class="border-none item" role="menuitemradio">
                  <a name="g_href" data-type="1" data-href="index.html#index_ads" data-redirect="Y" href="javascript:;">最新发布</a>
                </li>
                <li class="border-none item" role="menuitemradio">
                  <a name="g_href" data-type="6" data-href="queryDishonest/init" data-redirect="Y" href="javascript:;">信用信息</a>
                </li>
              </ul>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'
import { logout as apiLogout } from '@/api/auth'

const router = useRouter()
const searchKeyword = ref('')
const searchActive = ref(false)
const searchHistory = ref(['动车组介绍', '正晚点查询', '代售点'])
const suggestions = ref(['购票', '改签', '退票', '起售时间'])
const filteredSuggestions = computed(() => {
  const kw = searchKeyword.value.trim()
  if (!kw) return suggestions.value
  return suggestions.value.filter(s => s.includes(kw))
})

// 我的12306 下拉菜单交互优化
const my12306Active = ref(false)
let my12306Timer = null

const showMy12306 = () => {
  if (my12306Timer) {
    clearTimeout(my12306Timer)
    my12306Timer = null
  }
  my12306Active.value = true
}

const hideMy12306 = () => {
  my12306Timer = setTimeout(() => {
    my12306Active.value = false
  }, 200) // 延迟200ms隐藏，防止鼠标划出瞬间消失
}

const onSearchBlur = () => {
  // 延迟关闭，保证选择项点击可用
  setTimeout(() => (searchActive.value = false), 120)
}
const handleSearch = () => {
  const kw = searchKeyword.value.trim()
  if (!kw) return
  searchHistory.value.unshift(kw)
}
const applyHistory = kw => {
  searchKeyword.value = kw
  handleSearch()
}
const applySuggestion = kw => {
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
const openTicket = type => {
  if (type === 'dc') {
    router.push({ path: '/leftTicket/single' })
  } else {
    router.push({ path: '/leftTicket/round' })
  }
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
const goMy12306 = () => router.push({ path: '/user/profile', query: { group: '个人中心' } })
const goOrderInquiry = () => router.push('/user/orders')
const goPassengers = () => router.push('/user/passengers')
const goProfile = () => router.push({ path: '/user/profile', query: { group: '个人中心' } })

// 登录态与用户名显示
const userStore = useUserStore()
const { user, isAuthenticated } = storeToRefs(userStore)
const displayName = computed(() => {
  const u = user.value || {}
  return u.nickname || u.username || u.name || '用户'
})

const handleLogout = async () => {
  try {
    await apiLogout()
  } catch (e) {
    // ignore api error
  }
  await userStore.logout()
  router.push('/')
}

// 远程 logo 加载失败回退到本地 /pics/logo@2x.png
const tryLoadImage = url =>
  new Promise((resolve, reject) => {
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
/* 引入 12306 官方样式 (通用) */
@import '@/assets/12306-passenger/ticket_public_v70001.css';
@import '@/assets/12306-homepage/index_y_v50003.css';

/* 引入提取的头部专用样式 (包含布局修正与本地化) */
@import '@/assets/12306-homepage/header.css';
</style>
