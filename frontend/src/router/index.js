/**
 * Vue Router Configuration
 */
import { createRouter, createWebHistory } from 'vue-router'
import { permissionGuard, adminGuard, superAdminGuard } from './guards'

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
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/auth/ForgotPasswordPage.vue'),
      meta: { title: '找回密码' }
    },
    {
      path: '/trains',
      name: 'trains',
      component: () => import('@/views/train/TrainList.vue'),
      meta: { title: '车次列表' }
    },
    {
      path: '/permission-test',
      name: 'permission-test',
      component: () => import('@/views/PermissionTest.vue'),
      meta: { title: '权限测试', requiresAuth: true }
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
    // 合并本地新增：订单查询
    {
      path: '/order/inquiry',
      name: 'order-inquiry',
      component: () => import('@/views/order/OrderInquiry.vue'),
      meta: { title: '订单查询', requiresAuth: true }
    },
    {
      path: '/user',
      component: () => import('@/views/user/UserLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: { path: '/user/profile', query: { group: '个人中心' } }
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
      path: '/admin',
      component: () => import('@/views/admin/AdminLayout.vue'),
      meta: {
        requiresAuth: true,
        roles: ['admin', 'super_admin'],
        title: '管理后台'
      },
      beforeEnter: adminGuard,
      children: [
        {
          path: '',
          redirect: '/admin/dashboard'
        },
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: () => import('@/views/admin/Dashboard.vue'),
          meta: { title: '管理面板' }
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('@/views/admin/UserManagement.vue'),
          meta: {
            title: '用户管理',
            permissions: 'user:read'
          }
        },
        {
          path: 'roles',
          name: 'admin-roles',
          component: () => import('@/views/admin/RoleManagement.vue'),
          meta: {
            title: '角色管理',
            permissions: 'role:read'
          }
        },
        {
          path: 'permissions',
          name: 'admin-permissions',
          component: () => import('@/views/admin/PermissionManagement.vue'),
          meta: {
            title: '权限管理',
            permissions: 'permission:read'
          }
        },
        {
          path: 'trains',
          name: 'admin-trains',
          component: () => import('@/views/admin/TrainManagement.vue'),
          meta: {
            title: '车次管理',
            permissions: 'train:read'
          }
        },
        {
          path: 'orders',
          name: 'admin-orders',
          component: () => import('@/views/admin/OrderManagement.vue'),
          meta: {
            title: '订单管理',
            permissions: 'order:read'
          }
        },
        {
          path: 'system',
          name: 'admin-system',
          component: () => import('@/views/admin/SystemSettings.vue'),
          meta: {
            title: '系统设置',
            roles: 'super_admin'
          },
          beforeEnter: superAdminGuard
        }
      ]
    },
    // 合并本地新增：时刻表与服务类功能、信息页、测试/演示页
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
router.beforeEach(permissionGuard)

export default router
