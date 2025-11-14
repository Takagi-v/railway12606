/**
 * Permission Management API
 * 权限管理API接口
 */
import request from "@/utils/request";

// 权限管理API
export const permissionApi = {
  // 获取权限列表
  getPermissions: (params = {}) => {
    return request({
      url: "/permissions/",
      method: "get",
      params,
    });
  },

  // 根据ID获取权限
  getPermissionById: (id) => {
    return request({
      url: `/permissions/${id}`,
      method: "get",
    });
  },

  // 创建权限
  createPermission: (data) => {
    return request({
      url: "/permissions/",
      method: "post",
      data,
    });
  },

  // 更新权限
  updatePermission: (id, data) => {
    return request({
      url: `/permissions/${id}`,
      method: "put",
      data,
    });
  },

  // 删除权限
  deletePermission: (id) => {
    return request({
      url: `/permissions/${id}`,
      method: "delete",
    });
  },

  // 根据资源搜索权限
  searchPermissionsByResource: (resource) => {
    return request({
      url: `/permissions/search/resource/${resource}`,
      method: "get",
    });
  },

  // 根据操作搜索权限
  searchPermissionsByAction: (action) => {
    return request({
      url: `/permissions/search/action/${action}`,
      method: "get",
    });
  },
};

// 角色管理API
export const roleApi = {
  // 获取角色列表
  getRoles: (params = {}) => {
    return request({
      url: "/roles/",
      method: "get",
      params,
    });
  },

  // 根据ID获取角色
  getRoleById: (id) => {
    return request({
      url: `/roles/${id}`,
      method: "get",
    });
  },

  // 创建角色
  createRole: (data) => {
    return request({
      url: "/roles/",
      method: "post",
      data,
    });
  },

  // 更新角色
  updateRole: (id, data) => {
    return request({
      url: `/roles/${id}`,
      method: "put",
      data,
    });
  },

  // 删除角色
  deleteRole: (id) => {
    return request({
      url: `/roles/${id}`,
      method: "delete",
    });
  },

  // 获取角色的权限
  getRolePermissions: (id) => {
    return request({
      url: `/roles/${id}/permissions`,
      method: "get",
    });
  },

  // 为角色分配权限
  assignPermissionsToRole: (id, permissionIds) => {
    return request({
      url: `/roles/${id}/permissions`,
      method: "post",
      data: permissionIds,
    });
  },

  // 从角色移除权限
  removePermissionFromRole: (roleId, permissionId) => {
    return request({
      url: `/roles/${roleId}/permissions/${permissionId}`,
      method: "delete",
    });
  },

  // 批量分配权限
  batchAssignPermissions: (id, permissionIds) => {
    return request({
      url: `/roles/${id}/permissions/batch`,
      method: "post",
      data: { permission_ids: permissionIds },
    });
  },
};

// 用户角色管理API
export const userRoleApi = {
  // 获取用户角色
  getUserRoles: (userId) => {
    return request({
      url: `/user-roles/${userId}/roles`,
      method: "get",
    });
  },

  // 为用户分配角色
  assignRolesToUser: (userId, roleIds) => {
    return request({
      url: `/user-roles/${userId}/roles`,
      method: "post",
      data: roleIds,
    });
  },

  // 为用户分配单个角色
  assignSingleRoleToUser: (userId, roleId) => {
    return request({
      url: `/user-roles/${userId}/roles/${roleId}`,
      method: "post",
    });
  },

  // 从用户移除角色
  removeRoleFromUser: (userId, roleId) => {
    return request({
      url: `/user-roles/${userId}/roles/${roleId}`,
      method: "delete",
    });
  },

  // 获取用户权限
  getUserPermissions: (userId) => {
    return request({
      url: `/user-roles/${userId}/permissions`,
      method: "get",
    });
  },

  // 检查用户权限
  checkUserPermission: (userId, permissionCode) => {
    return request({
      url: `/user-roles/${userId}/permissions/check`,
      method: "post",
      data: { permission_code: permissionCode },
    });
  },

  // 检查用户角色
  checkUserRole: (userId, roleName) => {
    return request({
      url: `/user-roles/${userId}/roles/check`,
      method: "post",
      data: { role_name: roleName },
    });
  },

  // 获取所有用户角色信息
  getAllUsersRoles: () => {
    return request({
      url: "/user-roles/",
      method: "get",
    });
  },

  // 获取拥有指定角色的用户
  getRoleUsers: (roleId) => {
    return request({
      url: `/user-roles/roles/${roleId}/users`,
      method: "get",
    });
  },
};

// 权限常量定义
export const PERMISSIONS = {
  // 用户管理权限
  USER_READ: "user:read",
  USER_CREATE: "user:create",
  USER_UPDATE: "user:update",
  USER_DELETE: "user:delete",
  USER_MANAGE: "user:manage",

  // 角色管理权限
  ROLE_READ: "role:read",
  ROLE_CREATE: "role:create",
  ROLE_UPDATE: "role:update",
  ROLE_DELETE: "role:delete",
  ROLE_MANAGE: "role:manage",

  // 权限管理权限
  PERMISSION_READ: "permission:read",
  PERMISSION_CREATE: "permission:create",
  PERMISSION_UPDATE: "permission:update",
  PERMISSION_DELETE: "permission:delete",
  PERMISSION_MANAGE: "permission:manage",

  // 订单管理权限
  ORDER_READ: "order:read",
  ORDER_CREATE: "order:create",
  ORDER_UPDATE: "order:update",
  ORDER_DELETE: "order:delete",
  ORDER_MANAGE: "order:manage",

  // 车次管理权限
  TRAIN_READ: "train:read",
  TRAIN_CREATE: "train:create",
  TRAIN_UPDATE: "train:update",
  TRAIN_DELETE: "train:delete",
  TRAIN_MANAGE: "train:manage",

  // 系统管理权限
  SYSTEM_ADMIN: "system:admin",
};

// 角色常量定义
export const ROLES = {
  SUPER_ADMIN: "super_admin",
  ADMIN: "admin",
  MANAGER: "manager",
  USER: "user",
  GUEST: "guest",
};
