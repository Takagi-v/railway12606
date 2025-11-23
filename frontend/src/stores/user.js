/**
 * User Store
 * 用户状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import Cookies from 'js-cookie'
import {
  login as apiLogin,
  register as apiRegister,
  getUserProfile,
  refreshToken as apiRefreshToken
} from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const token = ref(Cookies.get('token') || null)
  const refreshToken = ref(Cookies.get('refreshToken') || null)
  const tokenExpiry = ref(Cookies.get('tokenExpiry') || null)
  const isAuthenticated = ref(!!token.value)
  const loginTime = ref(Cookies.get('loginTime') || null)
  const lastActivity = ref(Date.now())

  // Computed
  const isTokenExpired = computed(() => {
    if (!tokenExpiry.value) return false
    return Date.now() > parseInt(tokenExpiry.value)
  })

  const sessionTimeRemaining = computed(() => {
    if (!loginTime.value) return 0
    const sessionDuration = 24 * 60 * 60 * 1000 // 24 hours
    const elapsed = Date.now() - parseInt(loginTime.value)
    return Math.max(0, sessionDuration - elapsed)
  })

  // Actions
  const login = async credentials => {
    try {
      const response = await apiLogin(credentials)
      if (response.code === 200 || response.code === 201) {
        const { access_token, refresh_token, expires_in } = response.data

        // Calculate token expiry time
        const expiryTime = Date.now() + (expires_in || 3600) * 1000
        const currentTime = Date.now()

        // Store tokens and auth state
        token.value = access_token
        refreshToken.value = refresh_token
        tokenExpiry.value = expiryTime.toString()
        loginTime.value = currentTime.toString()
        isAuthenticated.value = true
        lastActivity.value = currentTime

        // Store in cookies with appropriate expiry
        const cookieOptions = {
          expires: 7,
          secure: typeof window !== 'undefined' && window.location.protocol === 'https:',
          sameSite: 'strict'
        }
        Cookies.set('token', access_token, cookieOptions)
        Cookies.set('refreshToken', refresh_token, cookieOptions)
        Cookies.set('tokenExpiry', expiryTime.toString(), cookieOptions)
        Cookies.set('loginTime', currentTime.toString(), cookieOptions)

        // Fetch user profile
        await fetchUserProfile()

        // Start session monitoring
        startSessionMonitoring()

        return response
      }
      throw new Error(response.message || '登录失败')
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const register = async userData => {
    try {
      const response = await apiRegister(userData)
      if (response.code === 200 || response.code === 201) {
        return response
      }
      throw new Error(response.message || '注册失败')
    } catch (error) {
      console.error('Register error:', error)
      throw error
    }
  }

  const fetchUserProfile = async () => {
    try {
      const response = await getUserProfile()
      if (response.code === 200) {
        user.value = response.data

        // 加载用户权限信息
        const { usePermissionStore } = await import('./permission')
        const permissionStore = usePermissionStore()
        await permissionStore.loadUserPermissions(user.value.id)
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
      // If profile fetch fails due to auth, try to refresh token
      if (error.response?.status === 401) {
        await handleTokenRefresh()
      }
    }
  }

  const handleTokenRefresh = async () => {
    try {
      if (!refreshToken.value) {
        throw new Error('No refresh token available')
      }

      const response = await apiRefreshToken(refreshToken.value)
      if (response.code === 200) {
        const { access_token, expires_in } = response.data
        const expiryTime = Date.now() + (expires_in || 3600) * 1000

        token.value = access_token
        tokenExpiry.value = expiryTime.toString()
        lastActivity.value = Date.now()

        // Update cookies
        const cookieOptions = {
          expires: 7,
          secure: typeof window !== 'undefined' && window.location.protocol === 'https:',
          sameSite: 'strict'
        }
        Cookies.set('token', access_token, cookieOptions)
        Cookies.set('tokenExpiry', expiryTime.toString(), cookieOptions)

        return true
      }
      throw new Error('Token refresh failed')
    } catch (error) {
      console.error('Token refresh error:', error)
      // If refresh fails, logout user
      logout()
      return false
    }
  }

  const logout = async (showMessage = true) => {
    user.value = null
    token.value = null
    refreshToken.value = null
    tokenExpiry.value = null
    loginTime.value = null
    isAuthenticated.value = false
    lastActivity.value = 0

    // Clear cookies
    Cookies.remove('token')
    Cookies.remove('refreshToken')
    Cookies.remove('tokenExpiry')
    Cookies.remove('loginTime')

    // Clear permission data
    try {
      const { usePermissionStore } = await import('./permission')
      const permissionStore = usePermissionStore()
      permissionStore.clearPermissions()
    } catch (error) {
      console.warn('清空权限数据失败:', error)
    }

    // Stop session monitoring
    stopSessionMonitoring()

    if (showMessage) {
      // You can add a message here if needed
      console.log('用户已安全退出')
    }
  }

  const updateActivity = () => {
    lastActivity.value = Date.now()
  }

  // Session monitoring
  let sessionTimer = null
  let activityTimer = null

  const startSessionMonitoring = () => {
    // Check for token expiry every minute
    sessionTimer = setInterval(() => {
      if (isTokenExpired.value) {
        handleTokenRefresh()
      }
    }, 60000)

    // Check for inactivity every 5 minutes
    activityTimer = setInterval(
      () => {
        const inactiveTime = Date.now() - lastActivity.value
        const maxInactiveTime = 30 * 60 * 1000 // 30 minutes

        if (inactiveTime > maxInactiveTime) {
          logout()
          // Redirect to login page or show session expired message
          window.location.href = '/login?reason=session_expired'
        }
      },
      5 * 60 * 1000
    )
  }

  const stopSessionMonitoring = () => {
    if (sessionTimer) {
      clearInterval(sessionTimer)
      sessionTimer = null
    }
    if (activityTimer) {
      clearInterval(activityTimer)
      activityTimer = null
    }
  }

  // Initialize user if token exists and is valid
  if (token.value && !isTokenExpired.value) {
    fetchUserProfile()
    startSessionMonitoring()
  } else if (token.value && isTokenExpired.value) {
    // Try to refresh token on initialization
    handleTokenRefresh()
  }

  // Listen for user activity
  if (typeof window !== 'undefined') {
    const activityEvents = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']
    const throttledUpdateActivity = throttle(updateActivity, 1000)

    activityEvents.forEach(event => {
      document.addEventListener(event, throttledUpdateActivity, true)
    })
  }

  return {
    // State
    user,
    token,
    refreshToken,
    isAuthenticated,
    loginTime,
    lastActivity,

    // Computed
    isTokenExpired,
    sessionTimeRemaining,

    // Actions
    login,
    register,
    logout,
    fetchUserProfile,
    handleTokenRefresh,
    updateActivity
  }
})

// Utility function for throttling
function throttle(func, limit) {
  let inThrottle
  return function () {
    const args = arguments
    const context = this
    if (!inThrottle) {
      func.apply(context, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}
