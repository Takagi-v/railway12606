/**
 * Axios Request Configuration
 * HTTP请求封装
 */
import router from '@/router'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'
import axios from 'axios'

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 添加认证token
    const userStore = useUserStore()
    const token = userStore.token

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // 添加时间戳防止缓存
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }

    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const { data } = response

    // 如果是文件下载，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }

    // 统一处理响应格式
    if (data.code !== undefined) {
      if (data.code === 200 || data.code === 201 || data.code === 0) {
        return data // 返回完整的响应对象，包括code、message和data
      } else {
        message.error(data.message || '请求失败')
        return Promise.reject(new Error(data.message || '请求失败'))
      }
    }

    return data
  },
  error => {
    console.error('Response error:', error)

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 400:
          message.error(data?.detail || data?.message || '请求参数错误')
          break;

        case 401:
          // 未授权，清除token并跳转到登录页
          const userStore = useUserStore()
          userStore.logout()
          // 优先显示后端返回的具体错误信息（如：密码错误、证件号不匹配等），如果没有则显示默认信息
          message.error(data?.detail || data?.message || '登录已过期，请重新登录')
          router.push('/login')
          break

        case 403:
          message.error('没有权限访问该资源')
          break

        case 404:
          message.error('请求的资源不存在')
          break

        case 422:
          // 表单验证错误
          if (data.detail && Array.isArray(data.detail)) {
            const errorMsg = data.detail.map(item => item.msg).join(', ')
            message.error(errorMsg)
          } else {
            message.error(data.message || '请求参数错误')
          }
          break

        case 429:
          message.error('请求过于频繁，请稍后再试')
          break

        case 500:
          message.error('服务器内部错误')
          break

        default:
          message.error(data?.detail || data?.message || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 网络错误
      message.error('网络连接失败，请检查网络设置')
    } else {
      // 其他错误
      const msg = error.message || '请求失败'
      // 过滤掉 Axios 默认的 "Request failed with status code xxx" 错误信息
      if (msg.startsWith('Request failed with status code')) {
         message.error('请求失败，请稍后重试')
      } else {
         message.error(msg)
      }
    }

    return Promise.reject(error)
  }
)

export default request
