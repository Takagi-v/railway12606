/**
 * Vue Router Configuration
 */
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Cookies from 'js-cookie'

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
      meta: { title: '订单填写', requiresAuth: true }
    },
    {
      path: '/order/:orderId',
      name: 'order-detail',
      component: () => import('@/views/order/OrderDetail.vue'),
      meta: { title: '订单详情', requiresAuth: true }
    },
    {
      path: '/user',
      component: () => import('@/views/user/UserLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/user/profile'
        },
        {
          path: 'profile',
          name: 'user-profile',
          component: () => import('@/views/user/ProfilePage.vue'),
          meta: { title: '个人信息' }
        },
        {
          path: 'passengers',
          name: 'user-passengers',
          component: () => import('@/views/user/PassengerPage.vue'),
          meta: { title: '乘客管理' }
        },
        {
          path: 'orders',
          name: 'user-orders',
          component: () => import('@/views/user/OrderPage.vue'),
          meta: { title: '订单管理' }
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

  // Check authentication
  const token = Cookies.get('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !token) {
    // Redirect to login if authentication is required
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
  } else if ((to.name === 'login' || to.name === 'register') && token) {
    // Redirect to home if already logged in
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
