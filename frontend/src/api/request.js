/**
 * Axios HTTP Client
 * HTTP请求封装
 */
import axios from 'axios'
import { message } from 'ant-design-vue'
import Cookies from 'js-cookie'
import router from '@/router'
import { ENV_CONFIG, isDebug } from '@/utils/env'

// Create axios instance
const request = axios.create({
  baseURL: ENV_CONFIG.API_BASE_URL,
  timeout: ENV_CONFIG.REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
request.interceptors.request.use(
  config => {
    // Add token to headers
    const token = Cookies.get('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 开发环境下打印请求信息
    if (isDebug()) {
      console.log('🚀 API Request:', {
        url: config.url,
        method: config.method,
        data: config.data,
        params: config.params
      })
    }
    
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
request.interceptors.response.use(
  response => {
    const res = response.data

    // 开发环境下打印响应信息
    if (isDebug()) {
      console.log('✅ API Response:', {
        url: response.config.url,
        status: response.status,
        data: res
      })
    }

    // If response code is not 200, treat it as an error
    if (res.code && res.code !== 200) {
      message.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || '请求失败'))
    }

    return res
  },
  error => {
    // 开发环境下打印错误信息
    if (isDebug()) {
      console.error('❌ API Error:', error)
    }

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          message.error('未登录或登录已过期，请重新登录')
          Cookies.remove('token')
          router.push({ name: 'login', query: { redirect: router.currentRoute.value.fullPath } })
          break
        case 403:
          message.error('没有权限访问')
          break
        case 404:
          message.error('请求的资源不存在')
          break
        case 500:
          message.error('服务器错误，请稍后重试')
          break
        default:
          message.error(data?.message || data?.detail || '请求失败')
      }
    } else if (error.request) {
      message.error('网络错误，请检查您的网络连接')
    } else {
      message.error('请求失败')
    }

    return Promise.reject(error)
  }
)

export default request
