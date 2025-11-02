/**
 * User Store
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import Cookies from 'js-cookie'
import { login as apiLogin, register as apiRegister, getUserProfile } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const token = ref(Cookies.get('token') || null)
  const isAuthenticated = ref(!!token.value)

  // Actions
  const login = async credentials => {
    const response = await apiLogin(credentials)
    if (response.code === 200) {
      token.value = response.data.access_token
      Cookies.set('token', token.value, { expires: 7 })
      isAuthenticated.value = true

      // Fetch user profile
      await fetchUserProfile()

      return response
    }
    throw new Error(response.message || '登录失败')
  }

  const register = async userData => {
    const response = await apiRegister(userData)
    if (response.code === 200) {
      return response
    }
    throw new Error(response.message || '注册失败')
  }

  const fetchUserProfile = async () => {
    try {
      const response = await getUserProfile()
      if (response.code === 200) {
        user.value = response.data
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    isAuthenticated.value = false
    Cookies.remove('token')
  }

  // Initialize user if token exists
  if (token.value) {
    fetchUserProfile()
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUserProfile
  }
})
