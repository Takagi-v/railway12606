/**
 * Permission Utilities
 * 权限工具类
 */
import { usePermissionStore } from '@/stores/permission'
import { useUserStore } from '@/stores/user'
import { PERMISSIONS, ROLES } from '@/api/permission'

/**
 * 权限检查工具类
 */
export class PermissionChecker {
  constructor() {
    this.permissionStore = null
    this.userStore = null
  }

  // 初始化store实例
  _initStores() {
    if (!this.permissionStore) {
      this.permissionStore = usePermissionStore()
    }
    if (!this.userStore) {
      this.userStore = useUserStore()
    }
  }

  /**
   * 检查是否具有指定权限
   * @param {string|string[]} permissions - 权限代码或权限代码数组
   * @param {string} mode - 检查模式：'any'(任一) 或 'all'(全部)
   * @returns {boolean}
   */
  hasPermission(permissions, mode = 'any') {
    this._initStores()
    
    if (!this.userStore.isAuthenticated) {
      return false
    }

    if (typeof permissions === 'string') {
      return this.permissionStore.hasPermission(permissions)
    }

    if (Array.isArray(permissions)) {
      return mode === 'all' 
        ? this.permissionStore.hasAllPermissions(permissions)
        : this.permissionStore.hasAnyPermission(permissions)
    }

    return false
  }

  /**
   * 检查是否具有指定角色
   * @param {string|string[]} roles - 角色名称或角色名称数组
   * @param {string} mode - 检查模式：'any'(任一) 或 'all'(全部)
   * @returns {boolean}
   */
  hasRole(roles, mode = 'any') {
    this._initStores()
    
    if (!this.userStore.isAuthenticated) {
      return false
    }

    if (typeof roles === 'string') {
      return this.permissionStore.hasRole(roles)
    }

    if (Array.isArray(roles)) {
      return mode === 'all' 
        ? this.permissionStore.hasAllRoles(roles)
        : this.permissionStore.hasAnyRole(roles)
    }

    return false
  }

  /**
   * 检查是否为管理员
   * @returns {boolean}
   */
  isAdmin() {
    this._initStores()
    return this.permissionStore.isAdmin
  }

  /**
   * 检查是否为超级管理员
   * @returns {boolean}
   */
  isSuperAdmin() {
    this._initStores()
    return this.permissionStore.isSuperAdmin
  }

  /**
   * 检查是否可以访问指定资源
   * @param {string} resource - 资源名称
   * @param {string} action - 操作类型
   * @returns {boolean}
   */
  canAccess(resource, action) {
    const permissionCode = `${resource}:${action}`
    return this.hasPermission(permissionCode)
  }

  /**
   * 检查是否可以管理指定资源
   * @param {string} resource - 资源名称
   * @returns {boolean}
   */
  canManage(resource) {
    return this.canAccess(resource, 'manage') || this.isSuperAdmin()
  }
}

/**
 * 权限装饰器工厂
 */
export class PermissionDecorator {
  /**
   * 创建权限检查装饰器
   * @param {string|string[]} permissions - 所需权限
   * @param {string} mode - 检查模式
   * @returns {Function}
   */
  static requirePermissions(permissions, mode = 'any') {
    return function(target, propertyKey, descriptor) {
      const originalMethod = descriptor.value
      
      descriptor.value = function(...args) {
        const checker = new PermissionChecker()
        
        if (!checker.hasPermission(permissions, mode)) {
          throw new Error(`权限不足：需要权限 ${Array.isArray(permissions) ? permissions.join(', ') : permissions}`)
        }
        
        return originalMethod.apply(this, args)
      }
      
      return descriptor
    }
  }

  /**
   * 创建角色检查装饰器
   * @param {string|string[]} roles - 所需角色
   * @param {string} mode - 检查模式
   * @returns {Function}
   */
  static requireRoles(roles, mode = 'any') {
    return function(target, propertyKey, descriptor) {
      const originalMethod = descriptor.value
      
      descriptor.value = function(...args) {
        const checker = new PermissionChecker()
        
        if (!checker.hasRole(roles, mode)) {
          throw new Error(`权限不足：需要角色 ${Array.isArray(roles) ? roles.join(', ') : roles}`)
        }
        
        return originalMethod.apply(this, args)
      }
      
      return descriptor
    }
  }
}

/**
 * 权限路由守卫
 */
export class PermissionGuard {
  /**
   * 检查路由权限
   * @param {Object} route - 路由对象
   * @param {Object} user - 用户对象
   * @returns {boolean}
   */
  static checkRoutePermission(route, user) {
    const checker = new PermissionChecker()
    
    // 如果路由没有权限要求，允许访问
    if (!route.meta?.permissions && !route.meta?.roles) {
      return true
    }

    // 检查权限要求
    if (route.meta.permissions) {
      const mode = route.meta.permissionMode || 'any'
      if (!checker.hasPermission(route.meta.permissions, mode)) {
        return false
      }
    }

    // 检查角色要求
    if (route.meta.roles) {
      const mode = route.meta.roleMode || 'any'
      if (!checker.hasRole(route.meta.roles, mode)) {
        return false
      }
    }

    return true
  }

  /**
   * 获取权限错误信息
   * @param {Object} route - 路由对象
   * @returns {string}
   */
  static getPermissionError(route) {
    const errors = []
    
    if (route.meta?.permissions) {
      errors.push(`需要权限: ${Array.isArray(route.meta.permissions) ? route.meta.permissions.join(', ') : route.meta.permissions}`)
    }
    
    if (route.meta?.roles) {
      errors.push(`需要角色: ${Array.isArray(route.meta.roles) ? route.meta.roles.join(', ') : route.meta.roles}`)
    }
    
    return errors.join('; ') || '权限不足'
  }
}

/**
 * 权限指令助手
 */
export class PermissionDirective {
  /**
   * 检查元素是否应该显示
   * @param {Object} binding - 指令绑定对象
   * @returns {boolean}
   */
  static shouldShow(binding) {
    const checker = new PermissionChecker()
    const { value, modifiers } = binding
    
    if (!value) return true
    
    // 检查权限
    if (value.permissions) {
      const mode = modifiers.all ? 'all' : 'any'
      if (!checker.hasPermission(value.permissions, mode)) {
        return false
      }
    }
    
    // 检查角色
    if (value.roles) {
      const mode = modifiers.all ? 'all' : 'any'
      if (!checker.hasRole(value.roles, mode)) {
        return false
      }
    }
    
    return true
  }
}

/**
 * 权限工具函数
 */
export const permissionUtils = {
  /**
   * 创建权限检查器实例
   * @returns {PermissionChecker}
   */
  createChecker() {
    return new PermissionChecker()
  },

  /**
   * 快速权限检查
   * @param {string|string[]} permissions - 权限代码
   * @param {string} mode - 检查模式
   * @returns {boolean}
   */
  check(permissions, mode = 'any') {
    const checker = new PermissionChecker()
    return checker.hasPermission(permissions, mode)
  },

  /**
   * 快速角色检查
   * @param {string|string[]} roles - 角色名称
   * @param {string} mode - 检查模式
   * @returns {boolean}
   */
  checkRole(roles, mode = 'any') {
    const checker = new PermissionChecker()
    return checker.hasRole(roles, mode)
  },

  /**
   * 检查是否为管理员
   * @returns {boolean}
   */
  isAdmin() {
    const checker = new PermissionChecker()
    return checker.isAdmin()
  },

  /**
   * 检查是否为超级管理员
   * @returns {boolean}
   */
  isSuperAdmin() {
    const checker = new PermissionChecker()
    return checker.isSuperAdmin()
  },

  /**
   * 获取权限显示名称
   * @param {string} permissionCode - 权限代码
   * @returns {string}
   */
  getPermissionName(permissionCode) {
    const permissionStore = usePermissionStore()
    return permissionStore.permissionUtils.formatPermissionName(permissionCode)
  },

  /**
   * 获取角色显示名称
   * @param {string} roleName - 角色名称
   * @returns {string}
   */
  getRoleName(roleName) {
    const permissionStore = usePermissionStore()
    return permissionStore.permissionUtils.formatRoleName(roleName)
  },

  /**
   * 权限常量
   */
  PERMISSIONS,
  
  /**
   * 角色常量
   */
  ROLES
}

// 导出单例实例
export const permissionChecker = new PermissionChecker()
export const permissionGuard = PermissionGuard
export const permissionDirective = PermissionDirective

// 默认导出
export default {
  PermissionChecker,
  PermissionDecorator,
  PermissionGuard,
  PermissionDirective,
  permissionUtils,
  permissionChecker,
  permissionGuard,
  permissionDirective
}