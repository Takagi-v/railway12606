/**
 * Authentication API
 * 认证相关的API接口
 */
import request from '@/utils/request'

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @param {string} data.username - 用户名/手机号
 * @param {string} data.password - 密码
 * @param {string} data.loginType - 登录类型 ('account' | 'phone')
 * @param {string} data.captcha - 验证码 (可选)
 * @returns {Promise}
 */
export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data: {
      ...data,
      timestamp: Date.now(),
      clientInfo: {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language
      }
    }
  })
}

/**
 * 手机验证码登录
 * @param {Object} data
 * @returns {Promise}
 */
export function loginWithSms(data) {
  return request({
    url: '/auth/login/sms',
    method: 'post',
    data
  })
}

/**
 * 二维码登录状态查询
 * @param {string} qrToken
 * @returns {Promise}
 */
export function checkQrLoginStatus(qrToken) {
  return request({
    url: `/auth/qr/status/${qrToken}`,
    method: 'get'
  })
}

/**
 * 获取二维码登录token
 * @returns {Promise}
 */
export function getQrLoginToken() {
  return request({
    url: '/auth/qr/generate',
    method: 'post'
  })
}

/**
 * 用户注册
 * @param {Object} data
 * @returns {Promise}
 */
export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data: {
      ...data,
      timestamp: Date.now()
    }
  })
}

/**
 * 发送手机验证码
 * @param {Object} data
 * @returns {Promise}
 */
export function sendSmsCode(data) {
  return request({
    url: '/auth/sms/send',
    method: 'post',
    data
  })
}

/**
 * 发送登录验证码 (校验身份证后4位)
 * @param {Object} data { username, idLast4 }
 * @returns {Promise}
 */
export function sendLoginVerifyCode(data) {
  return request({
    url: '/auth/login/verify-code',
    method: 'post',
    data: {
      username: data.username,
      id_last_4: data.idLast4
    }
  })
}

/**
 * 获取图形验证码
 * @returns {Promise}
 */
export function getCaptcha() {
  return request({
    url: '/auth/captcha',
    method: 'get'
  })
}

/**
 * 刷新访问令牌
 * @param {string} refreshToken
 * @returns {Promise}
 */
export function refreshToken(refreshToken) {
  return request({
    url: '/auth/refresh',
    method: 'post',
    data: {
      refresh_token: refreshToken
    }
  })
}

/**
 * 获取用户信息
 * @returns {Promise}
 */
export function getUserProfile() {
  return request({
    url: '/user/profile',
    method: 'get'
  })
}

/**
 * 更新用户信息
 * @param {Object} data
 * @returns {Promise}
 */
export function updateUserProfile(data) {
  return request({
    url: '/auth/profile',
    method: 'put',
    data
  })
}

/**
 * 修改密码
 * @param {Object} data
 * @returns {Promise}
 */
export function changePassword(data) {
  return request({
    url: '/auth/password/change',
    method: 'post',
    data
  })
}

/**
 * 重置密码 - 发送重置邮件/短信
 * @param {Object} data
 * @returns {Promise}
 */
export function requestPasswordReset(data) {
  return request({
    url: '/auth/password/reset/request',
    method: 'post',
    data
  })
}

/**
 * 重置密码 - 确认重置
 * @param {Object} data
 * @returns {Promise}
 */
export function confirmPasswordReset(data) {
  return request({
    url: '/auth/password/reset/confirm',
    method: 'post',
    data
  })
}

/**
 * 绑定手机号
 * @param {Object} data
 * @returns {Promise}
 */
export function bindPhone(data) {
  return request({
    url: '/auth/phone/bind',
    method: 'post',
    data
  })
}

/**
 * 解绑手机号
 * @param {Object} data
 * @returns {Promise}
 */
export function unbindPhone(data) {
  return request({
    url: '/auth/phone/unbind',
    method: 'post',
    data
  })
}

/**
 * 绑定邮箱
 * @param {Object} data
 * @returns {Promise}
 */
export function bindEmail(data) {
  return request({
    url: '/auth/email/bind',
    method: 'post',
    data
  })
}

/**
 * 用户退出登录
 * @returns {Promise}
 */
export function logout() {
  return request({
    url: '/auth/logout',
    method: 'post'
  })
}

/**
 * 检查用户名是否可用
 * @param {string} username
 * @returns {Promise}
 */
export function checkUsernameAvailability(username) {
  return request({
    url: `/auth/check/username/${username}`,
    method: 'get'
  })
}

/**
 * 检查手机号是否已注册
 * @param {string} phone
 * @returns {Promise}
 */
export function checkPhoneRegistered(phone) {
  return request({
    url: `/auth/check/phone/${phone}`,
    method: 'get'
  })
}

/**
 * 获取用户安全设置
 * @returns {Promise}
 */
export function getSecuritySettings() {
  return request({
    url: '/auth/security/settings',
    method: 'get'
  })
}

/**
 * 更新安全设置
 * @param {Object} data
 * @returns {Promise}
 */
export function updateSecuritySettings(data) {
  return request({
    url: '/auth/security/settings',
    method: 'put',
    data
  })
}

/**
 * 获取登录历史
 * @param {Object} params
 * @returns {Promise}
 */
export function getLoginHistory(params) {
  return request({
    url: '/auth/login/history',
    method: 'get',
    params
  })
}

/**
 * 人脸找回密码 - 提交身份信息
 * @param {Object} data
 * @returns {Promise}
 */
export function submitFaceRecovery(data) {
  return request({
    url: '/auth/password/recovery/face',
    method: 'post',
    data
  })
}

/**
 * 手机找回密码 - 提交身份信息
 * @param {Object} data
 * @returns {Promise}
 */
export function submitPhoneRecovery(data) {
  return request({
    url: '/auth/password/recovery/phone',
    method: 'post',
    data
  })
}

/**
 * 邮箱找回密码 - 提交身份信息
 * @param {Object} data
 * @returns {Promise}
 */
export function submitEmailRecovery(data) {
  return request({
    url: '/auth/password/recovery/email',
    method: 'post',
    data
  })
}

/**
 * 验证找回密码验证码
 * @param {Object} data
 * @returns {Promise}
 */
export function verifyRecoveryCode(data) {
  return request({
    url: '/auth/password/recovery/verify',
    method: 'post',
    data
  })
}

/**
 * 重发找回密码验证码
 * @param {Object} data { token }
 * @returns {Promise}
 */
export function resendRecoveryCode(data) {
  return request({
    url: '/auth/password/recovery/resend',
    method: 'post',
    data
  })
}

/**
 * 设置新密码
 * @param {Object} data
 * @returns {Promise}
 */
export function setNewPassword(data) {
  return request({
    url: '/auth/password/recovery/reset',
    method: 'post',
    data
  })
}
