import { usePermissionStore } from '@/stores/permission'
import { useUserStore } from '@/stores/user'

/**
 * 权限指令
 * 用法：
 * v-permission="'user:read'"
 * v-permission="['user:read', 'user:write']"
 * v-permission:any="['user:read', 'user:write']"
 * v-permission:all="['user:read', 'user:write']"
 * v-permission:role="'admin'"
 * v-permission:role:any="['admin', 'manager']"
 */
export const permissionDirective = {
  mounted(el, binding) {
    checkPermission(el, binding)
  },
  updated(el, binding) {
    checkPermission(el, binding)
  }
}

/**
 * 角色指令
 * 用法：
 * v-role="'admin'"
 * v-role="['admin', 'manager']"
 * v-role:any="['admin', 'manager']"
 * v-role:all="['admin', 'manager']"
 */
export const roleDirective = {
  mounted(el, binding) {
    checkRole(el, binding)
  },
  updated(el, binding) {
    checkRole(el, binding)
  }
}

/**
 * 权限或角色指令
 * 用法：
 * v-auth="{ permissions: 'user:read', roles: 'admin' }"
 * v-auth="{ permissions: ['user:read'], roles: ['admin'], mode: 'any' }"
 */
export const authDirective = {
  mounted(el, binding) {
    checkAuth(el, binding)
  },
  updated(el, binding) {
    checkAuth(el, binding)
  }
}

function checkPermission(el, binding) {
  const permissionStore = usePermissionStore()
  const userStore = useUserStore()
  
  // 如果用户未登录，隐藏元素
  if (!userStore.isAuthenticated) {
    hideElement(el)
    return
  }

  const { value, arg, modifiers } = binding
  
  if (!value) {
    return
  }

  let hasPermission = false

  if (Array.isArray(value)) {
    // 检查模式：any（任一）或 all（全部）
    const mode = Object.keys(modifiers)[0] || 'any'
    
    if (mode === 'all') {
      hasPermission = permissionStore.hasAllPermissions(value)
    } else {
      hasPermission = permissionStore.hasAnyPermission(value)
    }
  } else {
    hasPermission = permissionStore.hasPermission(value)
  }

  if (!hasPermission) {
    hideElement(el)
  } else {
    showElement(el)
  }
}

function checkRole(el, binding) {
  const permissionStore = usePermissionStore()
  const userStore = useUserStore()
  
  // 如果用户未登录，隐藏元素
  if (!userStore.isAuthenticated) {
    hideElement(el)
    return
  }

  const { value, modifiers } = binding
  
  if (!value) {
    return
  }

  let hasRole = false

  if (Array.isArray(value)) {
    // 检查模式：any（任一）或 all（全部）
    const mode = Object.keys(modifiers)[0] || 'any'
    
    if (mode === 'all') {
      hasRole = permissionStore.hasAllRoles(value)
    } else {
      hasRole = permissionStore.hasAnyRole(value)
    }
  } else {
    hasRole = permissionStore.hasRole(value)
  }

  if (!hasRole) {
    hideElement(el)
  } else {
    showElement(el)
  }
}

function checkAuth(el, binding) {
  const permissionStore = usePermissionStore()
  const userStore = useUserStore()
  
  // 如果用户未登录，隐藏元素
  if (!userStore.isAuthenticated) {
    hideElement(el)
    return
  }

  const { value } = binding
  
  if (!value || typeof value !== 'object') {
    return
  }

  const { permissions, roles, mode = 'any', requireAuth = true } = value

  // 如果需要登录但用户未登录
  if (requireAuth && !userStore.isAuthenticated) {
    hideElement(el)
    return
  }

  let hasAccess = true

  // 检查权限
  if (permissions) {
    let permissionCheck = false
    
    if (Array.isArray(permissions)) {
      permissionCheck = mode === 'all'
        ? permissionStore.hasAllPermissions(permissions)
        : permissionStore.hasAnyPermission(permissions)
    } else {
      permissionCheck = permissionStore.hasPermission(permissions)
    }
    
    hasAccess = hasAccess && permissionCheck
  }

  // 检查角色
  if (roles) {
    let roleCheck = false
    
    if (Array.isArray(roles)) {
      roleCheck = mode === 'all'
        ? permissionStore.hasAllRoles(roles)
        : permissionStore.hasAnyRole(roles)
    } else {
      roleCheck = permissionStore.hasRole(roles)
    }
    
    hasAccess = hasAccess && roleCheck
  }

  if (!hasAccess) {
    hideElement(el)
  } else {
    showElement(el)
  }
}

function hideElement(el) {
  // 保存原始显示状态
  if (!el._originalDisplay) {
    el._originalDisplay = el.style.display || ''
  }
  el.style.display = 'none'
}

function showElement(el) {
  // 恢复原始显示状态
  if (el._originalDisplay !== undefined) {
    el.style.display = el._originalDisplay
  } else {
    el.style.display = ''
  }
}

// 导出所有指令
export default {
  permission: permissionDirective,
  role: roleDirective,
  auth: authDirective
}