/**
 * Permission Store
 * 权限状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userRoleApi, PERMISSIONS, ROLES } from '@/api/permission'
import { useUserStore } from './user'

export const usePermissionStore = defineStore('permission', () => {
  // State
  const userPermissions = ref([])
  const userRoles = ref([])
  const permissionsLoaded = ref(false)
  const rolesLoaded = ref(false)
  const loading = ref(false)

  // Computed
  const hasPermissions = computed(() => userPermissions.value.length > 0)
  const hasRoles = computed(() => userRoles.value.length > 0)
  
  // 检查是否为超级管理员
  const isSuperAdmin = computed(() => {
    return userRoles.value.some(role => role.name === ROLES.SUPER_ADMIN)
  })
  
  // 检查是否为管理员
  const isAdmin = computed(() => {
    return userRoles.value.some(role => 
      role.name === ROLES.SUPER_ADMIN || role.name === ROLES.ADMIN
    )
  })
  
  // 检查是否为管理人员
  const isManager = computed(() => {
    return userRoles.value.some(role => 
      role.name === ROLES.SUPER_ADMIN || 
      role.name === ROLES.ADMIN || 
      role.name === ROLES.MANAGER
    )
  })

  // Actions
  const loadUserPermissions = async (userId = null) => {
    const userStore = useUserStore()
    const targetUserId = userId || userStore.user?.id
    
    if (!targetUserId) {
      console.warn('无法加载权限：用户ID不存在')
      return
    }

    try {
      loading.value = true
      const res = await userRoleApi.getUserPermissions(targetUserId)
      const data = res && res.data !== undefined ? res.data : res
      if (data) {
        userPermissions.value = data.permissions || []
        userRoles.value = data.roles || []
        permissionsLoaded.value = true
        rolesLoaded.value = true
      }
    } catch (error) {
      console.error('加载用户权限失败:', error)
      userPermissions.value = []
      userRoles.value = []
    } finally {
      loading.value = false
    }
  }

  const loadUserRoles = async (userId = null) => {
    const userStore = useUserStore()
    const targetUserId = userId || userStore.user?.id
    
    if (!targetUserId) {
      console.warn('无法加载角色：用户ID不存在')
      return
    }

    try {
      loading.value = true
      const res = await userRoleApi.getUserRoles(targetUserId)
      const data = res && res.data !== undefined ? res.data : res
      if (data && data.roles) {
        userRoles.value = data.roles || []
        rolesLoaded.value = true
      }
    } catch (error) {
      console.error('加载用户角色失败:', error)
      userRoles.value = []
    } finally {
      loading.value = false
    }
  }

  // 检查用户是否具有指定权限
  const hasPermission = (permissionCode) => {
    if (!permissionCode) return false
    
    // 超级管理员拥有所有权限
    if (isSuperAdmin.value) return true
    
    // 检查权限列表
    return userPermissions.value.some(permission => 
      permission.code === permissionCode && permission.is_active
    )
  }

  // 检查用户是否具有任一权限
  const hasAnyPermission = (permissionCodes) => {
    if (!Array.isArray(permissionCodes) || permissionCodes.length === 0) return false
    
    // 超级管理员拥有所有权限
    if (isSuperAdmin.value) return true
    
    return permissionCodes.some(code => hasPermission(code))
  }

  // 检查用户是否具有所有权限
  const hasAllPermissions = (permissionCodes) => {
    if (!Array.isArray(permissionCodes) || permissionCodes.length === 0) return false
    
    // 超级管理员拥有所有权限
    if (isSuperAdmin.value) return true
    
    return permissionCodes.every(code => hasPermission(code))
  }

  // 检查用户是否具有指定角色
  const hasRole = (roleName) => {
    if (!roleName) return false
    
    return userRoles.value.some(role => 
      role.name === roleName && role.is_active
    )
  }

  // 检查用户是否具有任一角色
  const hasAnyRole = (roleNames) => {
    if (!Array.isArray(roleNames) || roleNames.length === 0) return false
    
    return roleNames.some(name => hasRole(name))
  }

  // 检查用户是否具有所有角色
  const hasAllRoles = (roleNames) => {
    if (!Array.isArray(roleNames) || roleNames.length === 0) return false
    
    return roleNames.every(name => hasRole(name))
  }

  // 获取用户权限代码列表
  const getPermissionCodes = computed(() => {
    return userPermissions.value
      .filter(permission => permission.is_active)
      .map(permission => permission.code)
  })

  // 获取用户角色名称列表
  const getRoleNames = computed(() => {
    return userRoles.value
      .filter(role => role.is_active)
      .map(role => role.name)
  })

  // 检查是否可以访问管理功能
  const canAccessAdmin = computed(() => {
    return hasAnyRole([ROLES.SUPER_ADMIN, ROLES.ADMIN])
  })

  // 检查是否可以管理用户
  const canManageUsers = computed(() => {
    return hasAnyPermission([
      PERMISSIONS.USER_MANAGE,
      PERMISSIONS.USER_CREATE,
      PERMISSIONS.USER_UPDATE,
      PERMISSIONS.USER_DELETE
    ])
  })

  // 检查是否可以管理角色
  const canManageRoles = computed(() => {
    return hasAnyPermission([
      PERMISSIONS.ROLE_MANAGE,
      PERMISSIONS.ROLE_CREATE,
      PERMISSIONS.ROLE_UPDATE,
      PERMISSIONS.ROLE_DELETE
    ])
  })

  // 检查是否可以管理权限
  const canManagePermissions = computed(() => {
    return hasAnyPermission([
      PERMISSIONS.PERMISSION_MANAGE,
      PERMISSIONS.PERMISSION_CREATE,
      PERMISSIONS.PERMISSION_UPDATE,
      PERMISSIONS.PERMISSION_DELETE
    ])
  })

  // 检查是否可以管理订单
  const canManageOrders = computed(() => {
    return hasAnyPermission([
      PERMISSIONS.ORDER_MANAGE,
      PERMISSIONS.ORDER_CREATE,
      PERMISSIONS.ORDER_UPDATE,
      PERMISSIONS.ORDER_DELETE
    ])
  })

  // 检查是否可以管理车次
  const canManageTrains = computed(() => {
    return hasAnyPermission([
      PERMISSIONS.TRAIN_MANAGE,
      PERMISSIONS.TRAIN_CREATE,
      PERMISSIONS.TRAIN_UPDATE,
      PERMISSIONS.TRAIN_DELETE
    ])
  })

  // 远程检查权限（用于实时验证）
  const checkPermissionRemote = async (permissionCode, userId = null) => {
    const userStore = useUserStore()
    const targetUserId = userId || userStore.user?.id
    
    if (!targetUserId) return false

    try {
      const res = await userRoleApi.checkUserPermission(targetUserId, permissionCode)
      const data = res && res.data !== undefined ? res.data : res
      return !!(data && data.has_permission)
    } catch (error) {
      console.error('远程权限检查失败:', error)
      return false
    }
  }

  // 远程检查角色（用于实时验证）
  const checkRoleRemote = async (roleName, userId = null) => {
    const userStore = useUserStore()
    const targetUserId = userId || userStore.user?.id
    
    if (!targetUserId) return false

    try {
      const res = await userRoleApi.checkUserRole(targetUserId, roleName)
      const data = res && res.data !== undefined ? res.data : res
      return !!(data && data.has_role)
    } catch (error) {
      console.error('远程角色检查失败:', error)
      return false
    }
  }

  // 清空权限数据
  const clearPermissions = () => {
    userPermissions.value = []
    userRoles.value = []
    permissionsLoaded.value = false
    rolesLoaded.value = false
    loading.value = false
  }

  // 刷新权限数据
  const refreshPermissions = async (userId = null) => {
    clearPermissions()
    await loadUserPermissions(userId)
  }

  // 权限工具函数
  const permissionUtils = {
    // 格式化权限显示名称
    formatPermissionName: (permissionCode) => {
      const permissionMap = {
        [PERMISSIONS.USER_READ]: '查看用户',
        [PERMISSIONS.USER_CREATE]: '创建用户',
        [PERMISSIONS.USER_UPDATE]: '更新用户',
        [PERMISSIONS.USER_DELETE]: '删除用户',
        [PERMISSIONS.USER_MANAGE]: '管理用户',
        [PERMISSIONS.ROLE_READ]: '查看角色',
        [PERMISSIONS.ROLE_CREATE]: '创建角色',
        [PERMISSIONS.ROLE_UPDATE]: '更新角色',
        [PERMISSIONS.ROLE_DELETE]: '删除角色',
        [PERMISSIONS.ROLE_MANAGE]: '管理角色',
        [PERMISSIONS.PERMISSION_READ]: '查看权限',
        [PERMISSIONS.PERMISSION_CREATE]: '创建权限',
        [PERMISSIONS.PERMISSION_UPDATE]: '更新权限',
        [PERMISSIONS.PERMISSION_DELETE]: '删除权限',
        [PERMISSIONS.PERMISSION_MANAGE]: '管理权限',
        [PERMISSIONS.ORDER_READ]: '查看订单',
        [PERMISSIONS.ORDER_CREATE]: '创建订单',
        [PERMISSIONS.ORDER_UPDATE]: '更新订单',
        [PERMISSIONS.ORDER_DELETE]: '删除订单',
        [PERMISSIONS.ORDER_MANAGE]: '管理订单',
        [PERMISSIONS.TRAIN_READ]: '查看车次',
        [PERMISSIONS.TRAIN_CREATE]: '创建车次',
        [PERMISSIONS.TRAIN_UPDATE]: '更新车次',
        [PERMISSIONS.TRAIN_DELETE]: '删除车次',
        [PERMISSIONS.TRAIN_MANAGE]: '管理车次',
        [PERMISSIONS.SYSTEM_ADMIN]: '系统管理'
      }
      return permissionMap[permissionCode] || permissionCode
    },

    // 格式化角色显示名称
    formatRoleName: (roleName) => {
      const roleMap = {
        [ROLES.SUPER_ADMIN]: '超级管理员',
        [ROLES.ADMIN]: '管理员',
        [ROLES.MANAGER]: '业务管理员',
        [ROLES.USER]: '普通用户',
        [ROLES.GUEST]: '访客'
      }
      return roleMap[roleName] || roleName
    }
  }

  return {
    // State
    userPermissions,
    userRoles,
    permissionsLoaded,
    rolesLoaded,
    loading,

    // Computed
    hasPermissions,
    hasRoles,
    isSuperAdmin,
    isAdmin,
    isManager,
    getPermissionCodes,
    getRoleNames,
    canAccessAdmin,
    canManageUsers,
    canManageRoles,
    canManagePermissions,
    canManageOrders,
    canManageTrains,

    // Actions
    loadUserPermissions,
    loadUserRoles,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    hasRole,
    hasAnyRole,
    hasAllRoles,
    checkPermissionRemote,
    checkRoleRemote,
    clearPermissions,
    refreshPermissions,
    permissionUtils
  }
})