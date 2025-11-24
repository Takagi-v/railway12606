<template>
  <div class="architecture-test">
    <div class="test-header">
      <h1>架构改进测试页面</h1>
      <p>测试Pinia持久化、权限检查和路由守卫的功能</p>
    </div>

    <!-- Pinia 持久化测试 -->
    <div class="test-section">
      <h2>1. Pinia 持久化测试</h2>
      <div class="test-card">
        <h3>当前用户状态</h3>
        <div class="status-info">
          <p>
            <strong>认证状态:</strong>
            {{ isAuthenticated ? '已登录' : '未登录' }}
          </p>
          <p>
            <strong>用户信息:</strong>
            {{ user ? JSON.stringify(user, null, 2) : '无' }}
          </p>
          <p>
            <strong>Token:</strong>
            {{ token ? '存在' : '不存在' }}
          </p>
        </div>

        <div class="test-actions">
          <button @click="simulateLogin" class="btn-primary">模拟登录</button>
          <button @click="simulateLogout" class="btn-secondary">模拟登出</button>
          <button @click="refreshPage" class="btn-info">刷新页面测试持久化</button>
        </div>

        <div class="test-result">
          <p>
            <strong>测试说明:</strong>
            点击"模拟登录"后再点击"刷新页面测试持久化"，如果刷新后状态仍然保持，说明持久化功能正常。
          </p>
        </div>
      </div>
    </div>

    <!-- 权限检查测试 -->
    <div class="test-section">
      <h2>2. 权限检查测试</h2>
      <div class="test-card">
        <h3>当前用户权限</h3>
        <div class="permissions-info">
          <p>
            <strong>用户角色:</strong>
            {{ currentRole }}
          </p>
          <p><strong>拥有权限:</strong></p>
          <ul>
            <li v-for="permission in userPermissions" :key="permission">{{ permission }}</li>
          </ul>
        </div>

        <div class="permission-tests">
          <h4>权限测试</h4>
          <div class="permission-test" v-for="test in permissionTests" :key="test.name">
            <span>{{ test.name }}:</span>
            <span :class="test.hasPermission ? 'success' : 'error'">
              {{ test.hasPermission ? '✓ 有权限' : '✗ 无权限' }}
            </span>
          </div>
        </div>

        <div class="test-actions">
          <button @click="changeRole(USER_ROLES.GUEST)" class="btn-role">切换为游客</button>
          <button @click="changeRole(USER_ROLES.USER)" class="btn-role">切换为普通用户</button>
          <button @click="changeRole(USER_ROLES.VIP)" class="btn-role">切换为VIP用户</button>
          <button @click="changeRole(USER_ROLES.ADMIN)" class="btn-role">切换为管理员</button>
        </div>
      </div>
    </div>

    <!-- 路由守卫测试 -->
    <div class="test-section">
      <h2>3. 路由守卫测试</h2>
      <div class="test-card">
        <h3>路由访问测试</h3>
        <div class="route-tests">
          <div class="route-test" v-for="route in routeTests" :key="route.name">
            <div class="route-info">
              <strong>{{ route.name }}</strong>
              <span class="route-path">{{ route.path }}</span>
              <span class="route-auth">{{ route.requiresAuth ? '需要登录' : '公开访问' }}</span>
              <span v-if="route.permissions" class="route-permissions">
                需要权限: {{ route.permissions.join(', ') }}
              </span>
            </div>
            <div class="route-actions">
              <button @click="testRouteAccess(route)" class="btn-test">测试访问</button>
              <span :class="route.canAccess ? 'success' : 'error'">
                {{ route.canAccess ? '✓ 可访问' : '✗ 无法访问' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 测试日志 -->
    <div class="test-section">
      <h2>4. 测试日志</h2>
      <div class="test-card">
        <div class="test-logs">
          <div v-for="(log, index) in testLogs" :key="index" class="log-entry">
            <span class="log-time">{{ log.time }}</span>
            <span :class="'log-' + log.type">{{ log.message }}</span>
          </div>
        </div>
        <button @click="clearLogs" class="btn-secondary">清空日志</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  hasPermission,
  hasRole,
  canAccessRoute,
  getUserPermissions,
  USER_ROLES,
  PERMISSIONS
} from '@/utils/permission'

const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const testLogs = ref([])

// 计算属性
const isAuthenticated = computed(() => userStore.isAuthenticated)
const user = computed(() => userStore.user)
const token = computed(() => userStore.token)
const currentRole = computed(() => user.value?.role || 'GUEST')
const userPermissions = computed(() => getUserPermissions(user.value))

// 权限测试数据
const permissionTests = computed(() => [
  {
    name: '查看公开内容',
    hasPermission: hasPermission(PERMISSIONS.VIEW_PUBLIC, user.value)
  },
  {
    name: '创建订单',
    hasPermission: hasPermission(PERMISSIONS.CREATE_ORDER, user.value)
  },
  {
    name: '查看订单',
    hasPermission: hasPermission(PERMISSIONS.VIEW_ORDER, user.value)
  },
  {
    name: '管理乘客',
    hasPermission: hasPermission(PERMISSIONS.MANAGE_PASSENGERS, user.value)
  },
  {
    name: '查看个人资料',
    hasPermission: hasPermission(PERMISSIONS.VIEW_PROFILE, user.value)
  },
  {
    name: '管理员面板',
    hasPermission: hasPermission(PERMISSIONS.ADMIN_PANEL, user.value)
  }
])

// 路由测试数据
const routeTests = ref([
  {
    name: '首页',
    path: '/',
    requiresAuth: false,
    canAccess: true
  },
  {
    name: '登录页',
    path: '/login',
    requiresAuth: false,
    canAccess: true
  },
  {
    name: '订单创建',
    path: '/order/create',
    requiresAuth: true,
    permissions: [PERMISSIONS.CREATE_ORDER],
    canAccess: false
  },
  {
    name: '个人信息',
    path: '/user/profile',
    requiresAuth: true,
    permissions: [PERMISSIONS.VIEW_PROFILE],
    canAccess: false
  },
  {
    name: '乘客管理',
    path: '/user/passengers',
    requiresAuth: true,
    permissions: [PERMISSIONS.MANAGE_PASSENGERS],
    canAccess: false
  }
])

// 方法
const addLog = (message, type = 'info') => {
  testLogs.value.unshift({
    time: new Date().toLocaleTimeString(),
    message,
    type
  })
}

const simulateLogin = () => {
  const mockUser = {
    id: 1,
    username: 'testuser',
    email: 'test@example.com',
    role: USER_ROLES.USER // 使用正确的角色常量
  }

  // 直接修改store的状态
  userStore.user = mockUser
  userStore.token = 'mock-jwt-token'
  userStore.isAuthenticated = true

  addLog(`模拟登录成功，用户角色: ${USER_ROLES.USER}`, 'success')
  updateRouteTests()
}

const simulateLogout = () => {
  userStore.logout()
  addLog('用户已登出', 'info')
  updateRouteTests()
}

const refreshPage = () => {
  window.location.reload()
}

const changeRole = role => {
  if (!isAuthenticated.value) {
    addLog('请先登录再切换角色', 'error')
    return
  }

  const updatedUser = { ...user.value, role }
  userStore.user = updatedUser
  addLog(`角色已切换为: ${role}`, 'success')
  updateRouteTests()
}

const testRouteAccess = route => {
  const mockRoute = {
    path: route.path,
    meta: {
      requiresAuth: route.requiresAuth,
      permissions: route.permissions
    }
  }

  const canAccess = canAccessRoute(mockRoute, user.value)
  route.canAccess = canAccess

  const message = `测试路由 ${route.name} (${route.path}): ${canAccess ? '可访问' : '无法访问'}`
  addLog(message, canAccess ? 'success' : 'error')
}

const updateRouteTests = () => {
  routeTests.value.forEach(route => {
    testRouteAccess(route)
  })
}

const clearLogs = () => {
  testLogs.value = []
}

// 生命周期
onMounted(() => {
  addLog('架构测试页面已加载', 'info')
  updateRouteTests()
})
</script>

<style scoped>
.architecture-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-header {
  text-align: center;
  margin-bottom: 30px;
}

.test-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.test-section {
  margin-bottom: 30px;
}

.test-section h2 {
  color: #34495e;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.test-card {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.test-card h3 {
  color: #495057;
  margin-bottom: 15px;
}

.status-info,
.permissions-info {
  background: white;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 15px;
}

.status-info p,
.permissions-info p {
  margin: 5px 0;
}

.status-info ul,
.permissions-info ul {
  margin: 10px 0;
  padding-left: 20px;
}

.test-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 15px 0;
}

.btn-primary,
.btn-secondary,
.btn-info,
.btn-role,
.btn-test {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-role {
  background: #28a745;
  color: white;
}

.btn-test {
  background: #ffc107;
  color: #212529;
}

.permission-tests {
  margin: 15px 0;
}

.permission-test {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.route-tests {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.route-test {
  background: white;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.route-info {
  margin-bottom: 10px;
}

.route-info strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 5px;
}

.route-path {
  color: #6c757d;
  font-family: monospace;
  margin-right: 10px;
}

.route-auth,
.route-permissions {
  background: #e9ecef;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  margin-right: 5px;
}

.route-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.success {
  color: #28a745;
  font-weight: bold;
}

.error {
  color: #dc3545;
  font-weight: bold;
}

.test-result {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  border-radius: 4px;
  padding: 10px;
  margin-top: 15px;
}

.test-logs {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 15px;
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.log-entry {
  display: flex;
  gap: 10px;
  margin-bottom: 5px;
  font-family: monospace;
  font-size: 13px;
}

.log-time {
  color: #6c757d;
  min-width: 80px;
}

.log-info {
  color: #17a2b8;
}

.log-success {
  color: #28a745;
}

.log-error {
  color: #dc3545;
}
</style>
