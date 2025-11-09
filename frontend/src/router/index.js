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
          meta: { title: '乘客管理', permissions: 'passenger:read' }
        },
        {
          path: 'orders',
          name: 'user-orders',
          component: () => import('@/views/user/OrderPage.vue'),
          meta: { title: '订单管理', permissions: 'order:read' }
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

