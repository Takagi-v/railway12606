/**
 * Vue Router Configuration
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { canAccessRoute, PERMISSIONS } from '@/utils/permission'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomePage.vue'),
      meta: { title: '首页' }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/LoginPage.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/RegisterPage.vue'),
      meta: { title: '注册' }
    },
    {
      path: '/trains',
      name: 'trains',
      component: () => import('@/views/train/TrainList.vue'),
      meta: { title: '车次列表' }
    },
    {
      path: '/order/create',
      name: 'order-create',
      component: () => import('@/views/order/OrderCreate.vue'),
      meta: { 
        title: '订单填写', 
        requiresAuth: true,
        permissions: [PERMISSIONS.CREATE_ORDER]
      }
    },
    {
      path: '/order/:orderId',
      name: 'order-detail',
      component: () => import('@/views/order/OrderDetail.vue'),
      meta: { 
        title: '订单详情', 
        requiresAuth: true,
        permissions: [PERMISSIONS.VIEW_ORDER]
      }
    },
    {
      path: '/order/inquiry',
      name: 'order-inquiry',
      component: () => import('@/views/order/OrderInquiry.vue'),
      meta: { 
        title: '订单查询', 
        requiresAuth: true,
        permissions: [PERMISSIONS.VIEW_ORDER]
      }
    },
    {
      path: '/ticket/schedule',
      name: 'ticket-schedule',
      component: () => import('@/views/ticket/SchedulePage.vue'),
      meta: { title: '时刻表查询' }
    },
    {
      path: '/service/special-passenger',
      name: 'special-passenger',
      component: () => import('@/views/service/SpecialPassengerPage.vue'),
      meta: { title: '重点旅客预约', requiresAuth: true }
    },
    {
      path: '/service/lost-items',
      name: 'lost-items',
      component: () => import('@/views/service/LostItemsPage.vue'),
      meta: { title: '遗失物品查找', requiresAuth: true }
    },
    {
      path: '/service/car-booking',
      name: 'car-booking',
      component: () => import('@/views/service/CarServicePage.vue'),
      meta: { title: '约车服务', requiresAuth: true }
    },
    {
      path: '/service/shipping',
      name: 'shipping',
      component: () => import('@/views/service/ConvenientShippingPage.vue'),
      meta: { title: '便民托运', requiresAuth: true }
    },
    {
      path: '/service/station-guide',
      name: 'station-guide',
      component: () => import('@/views/service/StationGuidePage.vue'),
      meta: { title: '车站引导', requiresAuth: true }
    },
    {
      path: '/service/showcase',
      name: 'service-showcase',
      component: () => import('@/views/service/StationServicePage.vue'),
      meta: { title: '站车风采', requiresAuth: true }
    },
    {
      path: '/service/feedback',
      name: 'user-feedback',
      component: () => import('@/views/service/UserFeedbackPage.vue'),
      meta: { title: '用户反馈', requiresAuth: true }
    },
    {
      path: '/service/railway-pass',
      name: 'railway-pass',
      component: () => import('@/views/service/RailwayPassPage.vue'),
      meta: { title: '铁路畅行', requiresAuth: true }
    },
    {
      path: '/service/waitlist',
      name: 'waitlist-ticket',
      component: () => import('@/views/service/WaitlistPage.vue'),
      meta: { title: '候补购票', requiresAuth: true }
    },
    {
      path: '/announcement',
      name: 'announcement',
      component: () => import('@/views/info/AnnouncementPage.vue'),
      meta: { title: '公告信息' }
    },
    {
      path: '/faq',
      name: 'faq',
      component: () => import('@/views/info/FAQPage.vue'),
      meta: { title: '常见问题' }
    },
    {
      path: '/credit',
      name: 'credit',
      component: () => import('@/views/info/CreditPage.vue'),
      meta: { title: '信用信息' }
    },
    {
      path: '/user',
      component: () => import('@/views/user/UserLayout.vue'),
      meta: { 
        requiresAuth: true,
        permissions: [PERMISSIONS.VIEW_PROFILE]
      },
      children: [
        {
          path: '',
          redirect: '/user/profile'
        },
        {
          path: 'profile',
          name: 'user-profile',
          component: () => import('@/views/user/ProfilePage.vue'),
          meta: { 
            title: '个人信息',
            permissions: [PERMISSIONS.VIEW_PROFILE]
          }
        },
        {
          path: 'passengers',
          name: 'user-passengers',
          component: () => import('@/views/user/PassengerPage.vue'),
          meta: { 
            title: '乘客管理',
            permissions: [PERMISSIONS.MANAGE_PASSENGERS]
          }
        },
        {
          path: 'orders',
          name: 'user-orders',
          component: () => import('@/views/user/OrderPage.vue'),
          meta: { 
            title: '订单管理',
            permissions: [PERMISSIONS.VIEW_ORDER]
          }
        }
      ]
    },
    {
      path: '/env-test',
      name: 'env-test',
      component: () => import('@/views/test/EnvTest.vue'),
      meta: { title: '环境变量测试' }
    },
    {
      path: '/test/architecture',
      name: 'test-architecture',
      component: () => import('@/views/test/ArchitectureTest.vue'),
      meta: { title: '架构测试' }
    },
    {
      path: '/test/permission',
      name: 'test-permission',
      component: () => import('@/views/test/PermissionTest.vue'),
      meta: { title: '权限控制测试' }
    },
    {
      path: '/form-demo',
      name: 'form-demo',
      component: () => import('@/views/FormDemo.vue'),
      meta: { title: '表单组件演示' }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
      meta: { title: '页面未找到' }
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  // Set page title
  document.title = to.meta.title ? `${to.meta.title} - 中国铁路12306` : '中国铁路12306'

  // Get user store
  const userStore = useUserStore()
  const user = userStore.user
  const isAuthenticated = userStore.isAuthenticated

  // Check if route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated) {
    // Redirect to login if authentication is required
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // Redirect authenticated users away from auth pages
  if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    next({ name: 'home' })
    return
  }

  // Check route permissions
  if (!canAccessRoute(to, user)) {
    // If user is not authenticated, redirect to login
    if (!isAuthenticated) {
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
    } else {
      // If authenticated but no permission, redirect to home with error
      next({
        name: 'home',
        query: { error: 'no_permission' }
      })
    }
    return
  }

  next()
})

export default router
