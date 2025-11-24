/**
 * Environment Variables Utility
 * 环境变量工具函数
 */

/**
 * 获取环境变量值
 * @param {string} key - 环境变量键名
 * @param {any} defaultValue - 默认值
 * @returns {any} 环境变量值或默认值
 */
export const getEnv = (key, defaultValue = '') => {
  return import.meta.env[key] || defaultValue
}

/**
 * 获取布尔类型环境变量
 * @param {string} key - 环境变量键名
 * @param {boolean} defaultValue - 默认值
 * @returns {boolean} 布尔值
 */
export const getBooleanEnv = (key, defaultValue = false) => {
  const value = import.meta.env[key]
  if (value === undefined) return defaultValue
  return value === 'true' || value === true
}

/**
 * 获取数字类型环境变量
 * @param {string} key - 环境变量键名
 * @param {number} defaultValue - 默认值
 * @returns {number} 数字值
 */
export const getNumberEnv = (key, defaultValue = 0) => {
  const value = import.meta.env[key]
  if (value === undefined) return defaultValue
  const num = parseInt(value, 10)
  return isNaN(num) ? defaultValue : num
}

// 常用环境变量配置
export const ENV_CONFIG = {
  // API 配置
  API_BASE_URL: getEnv('VITE_API_BASE_URL', '/api'),
  REQUEST_TIMEOUT: getNumberEnv('VITE_REQUEST_TIMEOUT', 30000),

  // 应用配置
  APP_TITLE: getEnv('VITE_APP_TITLE', '中国铁路12306'),
  APP_VERSION: getEnv('VITE_APP_VERSION', '1.0.0'),
  NODE_ENV: getEnv('VITE_NODE_ENV', 'development'),

  // 功能开关
  DEBUG: getBooleanEnv('VITE_DEBUG', false),
  USE_MOCK: getBooleanEnv('VITE_USE_MOCK', false),

  // 业务配置
  UPLOAD_SIZE_LIMIT: getNumberEnv('VITE_UPLOAD_SIZE_LIMIT', 10),
  PAGE_SIZE: getNumberEnv('VITE_PAGE_SIZE', 20),
  TOKEN_EXPIRE_HOURS: getNumberEnv('VITE_TOKEN_EXPIRE_HOURS', 24)
}

// 开发环境检查
export const isDev = () => ENV_CONFIG.NODE_ENV === 'development'
export const isProd = () => ENV_CONFIG.NODE_ENV === 'production'
export const isDebug = () => ENV_CONFIG.DEBUG

// 导出默认配置
export default ENV_CONFIG
