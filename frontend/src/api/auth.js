/**
 * Authentication API
 * 认证相关的API接口
 */
import request from "@/utils/request";

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @param {string} data.username - 用户名/手机号
 * @param {string} data.password - 密码
 * @param {string} data.loginType - 登录类型 ('account' | 'phone')
 * @param {string} data.captcha - 验证码 (可选)
 * @returns {Promise} 登录结果
 */
<<<<<<< HEAD
export const login = data => {
=======
export function login(data) {
>>>>>>> origin/feature/user-authentication
  return request({
    url: "/auth/login",
    method: "post",
    data: {
      ...data,
      timestamp: Date.now(),
      clientInfo: {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
      },
    },
  });
}

/**
 * 手机验证码登录
 * @param {Object} data - 登录数据
 * @param {string} data.phone - 手机号
 * @param {string} data.verificationCode - 验证码
 * @returns {Promise} 登录结果
 */
export function loginWithSms(data) {
  return request({
    url: "/auth/login/sms",
    method: "post",
    data,
  });
}

/**
 * 二维码登录状态查询
 * @param {string} qrToken - 二维码token
 * @returns {Promise} 登录状态
 */
export function checkQrLoginStatus(qrToken) {
  return request({
    url: `/auth/qr/status/${qrToken}`,
    method: "get",
  });
}

/**
 * 获取二维码登录token
 * @returns {Promise} 二维码token和图片
 */
export function getQrLoginToken() {
  return request({
    url: "/auth/qr/generate",
    method: "post",
  });
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @param {string} data.username - 用户名
 * @param {string} data.phone - 手机号
 * @param {string} data.password - 密码
 * @param {string} data.confirmPassword - 确认密码
 * @param {string} data.verificationCode - 手机验证码
 * @param {string} data.captcha - 图形验证码
 * @param {boolean} data.agreeTerms - 是否同意服务条款
 * @returns {Promise} 注册结果
 */
<<<<<<< HEAD
export const register = data => {
=======
export function register(data) {
>>>>>>> origin/feature/user-authentication
  return request({
    url: "/auth/register",
    method: "post",
    data: {
      ...data,
      timestamp: Date.now(),
    },
  });
}

/**
 * 发送手机验证码
 * @param {Object} data - 验证码数据
 * @param {string} data.phone - 手机号
 * @param {string} data.type - 验证码类型 ('register' | 'login' | 'reset')
 * @param {string} data.captcha - 图形验证码
 * @returns {Promise} 发送结果
 */
export function sendSmsCode(data) {
  return request({
    url: "/auth/sms/send",
    method: "post",
    data,
  });
}

/**
 * 获取图形验证码
 * @returns {Promise} 验证码图片和token
 */
export function getCaptcha() {
  return request({
    url: "/auth/captcha",
    method: "get",
  });
}

/**
 * 刷新访问令牌
 * @param {string} refreshToken - 刷新令牌
 * @returns {Promise} 新的访问令牌
 */
export function refreshToken(refreshToken) {
  return request({
    url: "/auth/refresh",
    method: "post",
    data: {
      refresh_token: refreshToken,
    },
  });
}

/**
 * 获取用户信息
 * @returns {Promise} 用户信息
 */
export function getUserProfile() {
  return request({
    url: "/user/profile",
    method: "get",
  });
}

/**
 * 更新用户信息
 * @param {Object} data - 用户信息
 * @param {string} data.nickname - 昵称
 * @param {string} data.email - 邮箱
 * @param {string} data.avatar - 头像URL
 * @param {Object} data.preferences - 用户偏好设置
 * @returns {Promise} 更新结果
 */
<<<<<<< HEAD
export const updateUserProfile = data => {
=======
export function updateUserProfile(data) {
>>>>>>> origin/feature/user-authentication
  return request({
    url: "/auth/profile",
    method: "put",
    data,
  });
}

/**
 * 修改密码
 * @param {Object} data - 密码数据
 * @param {string} data.oldPassword - 旧密码
 * @param {string} data.newPassword - 新密码
 * @param {string} data.confirmPassword - 确认新密码
 * @returns {Promise} 修改结果
 */
export function changePassword(data) {
  return request({
    url: "/auth/password/change",
    method: "post",
    data,
  });
}
<<<<<<< HEAD
=======

/**
 * 重置密码 - 发送重置邮件/短信
 * @param {Object} data - 重置数据
 * @param {string} data.identifier - 邮箱或手机号
 * @param {string} data.type - 重置方式 ('email' | 'sms')
 * @returns {Promise} 发送结果
 */
export function requestPasswordReset(data) {
  return request({
    url: "/auth/password/reset/request",
    method: "post",
    data,
  });
}

/**
 * 重置密码 - 确认重置
 * @param {Object} data - 重置数据
 * @param {string} data.token - 重置令牌
 * @param {string} data.newPassword - 新密码
 * @param {string} data.confirmPassword - 确认新密码
 * @returns {Promise} 重置结果
 */
export function confirmPasswordReset(data) {
  return request({
    url: "/auth/password/reset/confirm",
    method: "post",
    data,
  });
}

/**
 * 绑定手机号
 * @param {Object} data - 绑定数据
 * @param {string} data.phone - 手机号
 * @param {string} data.verificationCode - 验证码
 * @returns {Promise} 绑定结果
 */
export function bindPhone(data) {
  return request({
    url: "/auth/phone/bind",
    method: "post",
    data,
  });
}

/**
 * 解绑手机号
 * @param {Object} data - 解绑数据
 * @param {string} data.verificationCode - 验证码
 * @param {string} data.password - 密码确认
 * @returns {Promise} 解绑结果
 */
export function unbindPhone(data) {
  return request({
    url: "/auth/phone/unbind",
    method: "post",
    data,
  });
}

/**
 * 绑定邮箱
 * @param {Object} data - 绑定数据
 * @param {string} data.email - 邮箱
 * @param {string} data.verificationCode - 验证码
 * @returns {Promise} 绑定结果
 */
export function bindEmail(data) {
  return request({
    url: "/auth/email/bind",
    method: "post",
    data,
  });
}

/**
 * 用户退出登录
 * @returns {Promise} 退出结果
 */
export function logout() {
  return request({
    url: "/auth/logout",
    method: "post",
  });
}

/**
 * 检查用户名是否可用
 * @param {string} username - 用户名
 * @returns {Promise} 检查结果
 */
export function checkUsernameAvailability(username) {
  return request({
    url: `/auth/check/username/${username}`,
    method: "get",
  });
}

/**
 * 检查手机号是否已注册
 * @param {string} phone - 手机号
 * @returns {Promise} 检查结果
 */
export function checkPhoneRegistered(phone) {
  return request({
    url: `/auth/check/phone/${phone}`,
    method: "get",
  });
}

/**
 * 获取用户安全设置
 * @returns {Promise} 安全设置信息
 */
export function getSecuritySettings() {
  return request({
    url: "/auth/security/settings",
    method: "get",
  });
}

/**
 * 更新安全设置
 * @param {Object} data - 安全设置
 * @param {boolean} data.twoFactorEnabled - 是否启用双因素认证
 * @param {boolean} data.loginNotification - 是否启用登录通知
 * @param {Array} data.trustedDevices - 受信任设备列表
 * @returns {Promise} 更新结果
 */
export function updateSecuritySettings(data) {
  return request({
    url: "/auth/security/settings",
    method: "put",
    data,
  });
}

/**
 * 获取登录历史
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.limit - 每页数量
 * @returns {Promise} 登录历史
 */
export function getLoginHistory(params) {
  return request({
    url: "/auth/login/history",
    method: "get",
    params,
  });
}

/**
 * 人脸找回密码 - 提交身份信息
 * @param {Object} data - 身份信息
 * @param {string} data.email - 邮箱
 * @param {string} data.idType - 证件类型
 * @param {string} data.idNumber - 证件号码
 * @returns {Promise} 提交结果
 */
export function submitFaceRecovery(data) {
  return request({
    url: "/auth/password/recovery/face",
    method: "post",
    data,
  });
}

/**
 * 手机找回密码 - 提交身份信息
 * @param {Object} data - 身份信息
 * @param {string} data.phone - 手机号
 * @param {string} data.idType - 证件类型
 * @param {string} data.idNumber - 证件号码
 * @returns {Promise} 提交结果
 */
export function submitPhoneRecovery(data) {
  return request({
    url: "/auth/password/recovery/phone",
    method: "post",
    data,
  });
}

/**
 * 邮箱找回密码 - 提交身份信息
 * @param {Object} data - 身份信息
 * @param {string} data.email - 邮箱
 * @param {string} data.idType - 证件类型
 * @param {string} data.idNumber - 证件号码
 * @returns {Promise} 提交结果
 */
export function submitEmailRecovery(data) {
  return request({
    url: "/auth/password/recovery/email",
    method: "post",
    data,
  });
}

/**
 * 验证找回密码验证码
 * @param {Object} data - 验证数据
 * @param {string} data.token - 找回令牌
 * @param {string} data.verificationCode - 验证码
 * @param {string} data.type - 找回方式 ('face' | 'phone' | 'email')
 * @returns {Promise} 验证结果
 */
export function verifyRecoveryCode(data) {
  return request({
    url: "/auth/password/recovery/verify",
    method: "post",
    data,
  });
}

/**
 * 设置新密码
 * @param {Object} data - 密码数据
 * @param {string} data.token - 重置令牌
 * @param {string} data.newPassword - 新密码
 * @param {string} data.confirmPassword - 确认新密码
 * @returns {Promise} 设置结果
 */
export function setNewPassword(data) {
  return request({
    url: "/auth/password/recovery/reset",
    method: "post",
    data,
  });
}
>>>>>>> origin/feature/user-authentication
