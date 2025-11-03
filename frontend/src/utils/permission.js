/**
 * Permission Management Utilities
 * 权限管理工具
 */

// 用户类型枚举（根据12306需求文档）
export const USER_TYPES = {
  GUEST: 'guest',        // 游客（未登录）
  ADULT: 'adult',        // 成人用户
  STUDENT: 'student'     // 学生用户
}

// 权限枚举
export const PERMISSIONS = {
  // 基础权限
  VIEW_PUBLIC: 'view:public',           // 查看公开内容
  VIEW_TRAINS: 'view:trains',           // 查看车次信息
  
  // 用户权限（需要登录）
  CREATE_ORDER: 'create:order',         // 创建订单
  VIEW_ORDER: 'view:order',             // 查看订单
  CANCEL_ORDER: 'cancel:order',         // 取消订单
  REFUND_TICKET: 'refund:ticket',       // 退票
  
  // 个人信息权限
  VIEW_PROFILE: 'view:profile',         // 查看个人信息
  EDIT_PROFILE: 'edit:profile',         // 编辑个人信息
  MANAGE_PASSENGERS: 'manage:passengers', // 管理乘客信息
  
  // 服务权限
  USE_SERVICES: 'use:services',         // 使用增值服务
  SPECIAL_PASSENGER: 'special:passenger', // 重点旅客服务
  
  // 学生特殊权限
  STUDENT_DISCOUNT: 'student:discount', // 学生票优惠
  STUDENT_VERIFICATION: 'student:verification' // 学生身份验证
}

// 用户类型权限映射
export const TYPE_PERMISSIONS = {
  [USER_TYPES.GUEST]: [
    PERMISSIONS.VIEW_PUBLIC,
    PERMISSIONS.VIEW_TRAINS
  ],
  [USER_TYPES.ADULT]: [
    PERMISSIONS.VIEW_PUBLIC,
    PERMISSIONS.VIEW_TRAINS,
    PERMISSIONS.CREATE_ORDER,
    PERMISSIONS.VIEW_ORDER,
    PERMISSIONS.CANCEL_ORDER,
    PERMISSIONS.REFUND_TICKET,
    PERMISSIONS.VIEW_PROFILE,
    PERMISSIONS.EDIT_PROFILE,
    PERMISSIONS.MANAGE_PASSENGERS,
    PERMISSIONS.USE_SERVICES,
    PERMISSIONS.SPECIAL_PASSENGER
  ],
  [USER_TYPES.STUDENT]: [
    PERMISSIONS.VIEW_PUBLIC,
    PERMISSIONS.VIEW_TRAINS,
    PERMISSIONS.CREATE_ORDER,
    PERMISSIONS.VIEW_ORDER,
    PERMISSIONS.CANCEL_ORDER,
    PERMISSIONS.REFUND_TICKET,
    PERMISSIONS.VIEW_PROFILE,
    PERMISSIONS.EDIT_PROFILE,
    PERMISSIONS.MANAGE_PASSENGERS,
    PERMISSIONS.USE_SERVICES,
    PERMISSIONS.SPECIAL_PASSENGER,
    PERMISSIONS.STUDENT_DISCOUNT,
    PERMISSIONS.STUDENT_VERIFICATION
  ]
}

// 保持向后兼容性
export const USER_ROLES = USER_TYPES
export const ROLE_PERMISSIONS = TYPE_PERMISSIONS

/**
 * 检查用户是否有指定权限
 * @param {string} permission 权限标识
 * @param {Object} user 用户对象
 * @returns {boolean} 是否有权限
 */
export function hasPermission(permission, user = null) {
  if (!user) {
    // 未登录用户只有游客权限
    return TYPE_PERMISSIONS[USER_TYPES.GUEST].includes(permission)
  }
  
  // 根据用户类型获取权限，默认为成人用户
  const userType = user.user_type || user.userType || USER_TYPES.ADULT
  const userPermissions = TYPE_PERMISSIONS[userType] || TYPE_PERMISSIONS[USER_TYPES.ADULT]
  
  return userPermissions.includes(permission)
}

/**
 * 检查用户是否有指定类型
 * @param {string} type 用户类型标识
 * @param {Object} user 用户对象
 * @returns {boolean} 是否有该类型
 */
export function hasUserType(type, user = null) {
  if (!user) {
    return type === USER_TYPES.GUEST
  }
  
  const userType = user.user_type || user.userType || USER_TYPES.ADULT
  return userType === type
}

/**
 * 检查用户是否有指定角色（保持向后兼容）
 * @param {string} role 角色标识
 * @param {Object} user 用户对象
 * @returns {boolean} 是否有该角色
 */
export function hasRole(role, user = null) {
  return hasUserType(role, user)
}

/**
 * 检查用户是否可以访问指定路由
 * @param {Object} route 路由对象
 * @param {Object} user 用户对象
 * @returns {boolean} 是否可以访问
 */
export function canAccessRoute(route, user = null) {
  const { meta = {} } = route
  
  // 检查是否需要登录
  if (meta.requiresAuth && !user) {
    return false
  }
  
  // 检查用户类型要求
  if (meta.userTypes && meta.userTypes.length > 0) {
    return meta.userTypes.some(type => hasUserType(type, user))
  }
  
  // 检查角色要求（向后兼容）
  if (meta.roles && meta.roles.length > 0) {
    return meta.roles.some(role => hasUserType(role, user))
  }
  
  // 检查权限要求
  if (meta.permissions && meta.permissions.length > 0) {
    return meta.permissions.some(permission => hasPermission(permission, user))
  }
  
  return true
}

/**
 * 获取用户的所有权限
 * @param {Object} user 用户对象
 * @returns {Array} 权限列表
 */
export function getUserPermissions(user = null) {
  if (!user) {
    return TYPE_PERMISSIONS[USER_TYPES.GUEST]
  }
  
  const userType = user.user_type || user.userType || USER_TYPES.ADULT
  return TYPE_PERMISSIONS[userType] || TYPE_PERMISSIONS[USER_TYPES.ADULT]
}

/**
 * 检查用户是否已登录
 * @param {Object} user 用户对象
 * @returns {boolean} 是否已登录
 */
export function isAuthenticated(user = null) {
  return user !== null && user !== undefined
}

/**
 * 检查用户是否为学生
 * @param {Object} user 用户对象
 * @returns {boolean} 是否为学生
 */
export function isStudent(user = null) {
  return hasUserType(USER_TYPES.STUDENT, user)
}

/**
 * 检查用户是否为成人
 * @param {Object} user 用户对象
 * @returns {boolean} 是否为成人
 */
export function isAdult(user = null) {
  return hasUserType(USER_TYPES.ADULT, user)
}

/**
 * 权限指令工厂函数
 * 用于Vue指令 v-permission
 */
export function createPermissionDirective() {
  const checkPermission = (el, binding, vnode) => {
    // 尝试从多个来源获取用户状态
    let user = null;
    
    // 1. 尝试从组件实例的setupState获取（用于<script setup>）
    const instance = vnode.ctx;
    if (instance && instance.setupState) {
      const setupState = instance.setupState;
      
      // 检查computed属性 user
      if (setupState.user && typeof setupState.user === 'object' && setupState.user.value !== undefined) {
        user = setupState.user.value;
      }
      // 检查ref属性 testUser
      else if (setupState.testUser && setupState.testUser.value !== undefined) {
        user = setupState.testUser.value;
      }
      // 检查直接值
      else if (setupState.user) {
        user = setupState.user;
      }
    }
    
    // 2. 尝试从组件实例的data获取
    if (!user && instance && instance.data && instance.data.user) {
      user = instance.data.user;
    }
    
    // 3. 尝试从Pinia store获取
    if (!user) {
      try {
        const userStore = useUserStore();
        user = userStore.user;
      } catch (error) {
        // 忽略错误，继续使用null用户
      }
    }
    
    const permission = binding.value;
    const hasAccess = hasPermission(permission, user);
    
    if (!hasAccess) {
      el.style.display = 'none';
    } else {
      el.style.display = '';
    }
  };

  return {
    mounted(el, binding, vnode) {
      checkPermission(el, binding, vnode);
    },
    updated(el, binding, vnode) {
      checkPermission(el, binding, vnode);
    }
  };
}