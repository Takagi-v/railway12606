import { useUserStore } from '@/stores/user'
import { usePermissionStore } from '@/stores/permission'
import { message } from 'ant-design-vue'
import Cookies from 'js-cookie'

/**
 * 权限路由守卫
 * @param {Object} to 目标路由
 * @param {Object} from 来源路由
 * @param {Function} next 导航函数
 */
export async function permissionGuard(to, from, next) {
  const userStore = useUserStore()
  const permissionStore = usePermissionStore()

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 中国铁路12306` : '中国铁路12306'

  // 检查是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = Cookies.get('token')

  // 如果需要认证但没有token，跳转到登录页
  if (requiresAuth && !token) {
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // 如果已登录但访问登录/注册页，跳转到首页
  if ((to.name === 'login' || to.name === 'register') && token) {
    next({ name: 'home' })
    return
  }

  // 如果不需要权限检查，直接通过
  if (!requiresAuth && !to.meta.permissions && !to.meta.roles) {
    next()
    return
  }

  // 确保用户信息和权限已加载
  if (token && !userStore.user) {
    try {
      await userStore.fetchUserProfile()
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // 清除无效token
      userStore.logout()
      next({
        name: 'login',
        query: { redirect: to.fullPath }
      })
      return
    }
  }

  // 检查权限
  if (to.meta.permissions || to.meta.roles) {
    const hasAccess = await checkRoutePermission(to.meta, permissionStore)

    if (!hasAccess) {
      message.error('您没有访问此页面的权限')

      // 根据用户角色跳转到合适的页面
      if (permissionStore.isSuperAdmin || permissionStore.isAdmin) {
        next({ name: 'admin-dashboard' })
      } else if (permissionStore.isManager) {
        next({ name: 'manager-dashboard' })
      } else {
        next({ name: 'home' })
      }
      return
    }
  }

  next()
}

/**
 * 检查路由权限
 * @param {Object} meta 路由元信息
 * @param {Object} permissionStore 权限store
 * @returns {Promise<boolean>}
 */
async function checkRoutePermission(meta, permissionStore) {
  const { permissions, roles, permissionMode = 'any', roleMode = 'any' } = meta

  let hasPermission = true
  let hasRole = true

  // 检查权限
  if (permissions) {
    if (Array.isArray(permissions)) {
      hasPermission =
        permissionMode === 'all'
          ? permissionStore.hasAllPermissions(permissions)
          : permissionStore.hasAnyPermission(permissions)
    } else {
      hasPermission = permissionStore.hasPermission(permissions)
    }
  }

  // 检查角色
  if (roles) {
    if (Array.isArray(roles)) {
      hasRole =
        roleMode === 'all' ? permissionStore.hasAllRoles(roles) : permissionStore.hasAnyRole(roles)
    } else {
      hasRole = permissionStore.hasRole(roles)
    }
  }

  return hasPermission && hasRole
}

/**
 * 管理员路由守卫
 */
export function adminGuard(to, from, next) {
  const permissionStore = usePermissionStore()

  if (!permissionStore.isAdmin && !permissionStore.isSuperAdmin) {
    message.error('您没有访问管理后台的权限')
    next({ name: 'home' })
    return
  }

  next()
}

/**
 * 超级管理员路由守卫
 */
export function superAdminGuard(to, from, next) {
  const permissionStore = usePermissionStore()

  if (!permissionStore.isSuperAdmin) {
    message.error('您没有访问此功能的权限')
    next({ name: 'admin-dashboard' })
    return
  }

  next()
}
