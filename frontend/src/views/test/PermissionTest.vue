<template>
  <div class="permission-test">
    <div class="header">
      <h1>权限控制测试页面</h1>
      <p class="description">测试新的用户类型权限系统</p>
    </div>

    <!-- 用户状态显示 -->
    <div class="user-status">
      <h2>当前用户状态</h2>
      <div class="status-card">
        <div class="status-item">
          <label>登录状态:</label>
          <span :class="{ 'status-success': isAuthenticated, 'status-error': !isAuthenticated }">
            {{ isAuthenticated ? '已登录' : '未登录' }}
          </span>
        </div>
        <div class="status-item" v-if="user">
          <label>用户名:</label>
          <span>{{ user.username || '未知' }}</span>
        </div>
        <div class="status-item" v-if="user">
          <label>用户类型:</label>
          <span :class="`user-type-${user.user_type || user.userType || 'adult'}`">
            {{ getUserTypeLabel(user.user_type || user.userType || 'adult') }}
          </span>
        </div>
        <div class="status-item" v-if="!user">
          <label>用户类型:</label>
          <span class="user-type-guest">游客</span>
        </div>
      </div>
    </div>

    <!-- 用户类型切换 -->
    <div class="user-type-switcher">
      <h2>用户类型切换测试</h2>
      <div class="switcher-buttons">
        <button 
          @click="switchUserType('guest')" 
          :class="{ active: currentTestType === 'guest' }"
          class="btn btn-guest"
        >
          游客模式
        </button>
        <button 
          @click="switchUserType('adult')" 
          :class="{ active: currentTestType === 'adult' }"
          class="btn btn-adult"
        >
          成人用户
        </button>
        <button 
          @click="switchUserType('student')" 
          :class="{ active: currentTestType === 'student' }"
          class="btn btn-student"
        >
          学生用户
        </button>
      </div>
    </div>

    <!-- 权限测试 -->
    <div class="permission-tests">
      <h2>权限测试</h2>
      <div class="test-grid">
        <div class="test-card" v-for="permission in testPermissions" :key="permission.key">
          <h3>{{ permission.name }}</h3>
          <p class="permission-desc">{{ permission.description }}</p>
          <div class="permission-result">
            <span class="permission-key">{{ permission.key }}</span>
            <span 
              :class="{ 
                'result-success': hasPermissionTest(permission.key), 
                'result-error': !hasPermissionTest(permission.key) 
              }"
            >
              {{ hasPermissionTest(permission.key) ? '✓ 有权限' : '✗ 无权限' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户类型检查测试 -->
    <div class="user-type-tests">
      <h2>用户类型检查测试</h2>
      <div class="type-test-grid">
        <div class="type-test-card" v-for="type in userTypes" :key="type.key">
          <h3>{{ type.name }}</h3>
          <div class="type-result">
            <span 
              :class="{ 
                'result-success': hasUserTypeTest(type.key), 
                'result-error': !hasUserTypeTest(type.key) 
              }"
            >
              {{ hasUserTypeTest(type.key) ? '✓ 是' : '✗ 否' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 路由访问测试 -->
    <div class="route-tests">
      <h2>路由访问权限测试</h2>
      <div class="route-test-grid">
        <div class="route-test-card" v-for="route in testRoutes" :key="route.path">
          <h3>{{ route.name }}</h3>
          <p class="route-path">{{ route.path }}</p>
          <div class="route-meta" v-if="route.meta">
            <span v-if="route.meta.requiresAuth" class="meta-tag">需要登录</span>
            <span v-if="route.meta.userTypes" class="meta-tag">
              用户类型: {{ route.meta.userTypes.join(', ') }}
            </span>
            <span v-if="route.meta.permissions" class="meta-tag">
              权限: {{ route.meta.permissions.join(', ') }}
            </span>
          </div>
          <div class="route-result">
            <span 
              :class="{ 
                'result-success': canAccessRouteTest(route), 
                'result-error': !canAccessRouteTest(route) 
              }"
            >
              {{ canAccessRouteTest(route) ? '✓ 可访问' : '✗ 不可访问' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 权限指令测试 -->
    <div class="directive-tests">
      <h2>v-permission 指令测试</h2>
      <div class="directive-grid">
        <div class="directive-card">
          <h3>查看公共内容</h3>
          <div v-permission="PERMISSIONS.VIEW_PUBLIC" class="permission-content success">
            ✓ 这个内容对所有用户可见 (VIEW_PUBLIC)
          </div>
        </div>
        <div class="directive-card">
          <h3>创建订单</h3>
          <div v-permission="PERMISSIONS.CREATE_ORDER" class="permission-content success">
            ✓ 这个内容只有登录用户可见 (CREATE_ORDER)
          </div>
        </div>
        <div class="directive-card">
          <h3>学生优惠</h3>
          <div v-permission="PERMISSIONS.STUDENT_DISCOUNT" class="permission-content success">
            ✓ 这个内容只有学生用户可见 (STUDENT_DISCOUNT)
          </div>
        </div>
        <div class="directive-card">
          <h3>学生验证</h3>
          <div v-permission="PERMISSIONS.STUDENT_VERIFICATION" class="permission-content success">
            ✓ 这个内容只有学生用户可见 (STUDENT_VERIFICATION)
          </div>
        </div>
      </div>
    </div>

    <!-- 权限详情 -->
    <div class="permission-details">
      <h2>当前用户权限详情</h2>
      <div class="permissions-list">
        <div class="permission-item" v-for="permission in currentUserPermissions" :key="permission">
          <span class="permission-badge">{{ permission }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { 
  hasPermission, 
  hasUserType, 
  canAccessRoute, 
  getUserPermissions,
  isAuthenticated as checkAuthenticated,
  isStudent,
  isAdult,
  USER_TYPES,
  PERMISSIONS
} from '@/utils/permission'

const userStore = useUserStore()

// 测试用的用户类型状态
const currentTestType = ref('guest')
const testUser = ref(null)

// 计算属性
const user = computed(() => testUser.value || userStore.user)
const isAuthenticated = computed(() => testUser.value ? true : userStore.isAuthenticated)

// 用户类型标签映射
const getUserTypeLabel = (type) => {
  const labels = {
    guest: '游客',
    adult: '成人用户',
    student: '学生用户'
  }
  return labels[type] || '未知'
}

// 切换用户类型进行测试
const switchUserType = (type) => {
  currentTestType.value = type
  if (type === 'guest') {
    testUser.value = null
  } else {
    testUser.value = {
      id: 1,
      username: `test_${type}`,
      user_type: type,
      userType: type
    }
  }
}

// 测试权限
const testPermissions = [
  { key: PERMISSIONS.VIEW_PUBLIC, name: '查看公共内容', description: '所有用户都应该有此权限' },
  { key: PERMISSIONS.CREATE_ORDER, name: '创建订单', description: '只有登录用户才有此权限' },
  { key: PERMISSIONS.VIEW_ORDER, name: '查看订单', description: '只有登录用户才有此权限' },
  { key: PERMISSIONS.MANAGE_PASSENGERS, name: '管理乘客', description: '只有登录用户才有此权限' },
  { key: PERMISSIONS.VIEW_PROFILE, name: '查看个人信息', description: '只有登录用户才有此权限' },
  { key: PERMISSIONS.STUDENT_DISCOUNT, name: '学生优惠', description: '只有学生用户才有此权限' },
  { key: PERMISSIONS.STUDENT_VERIFICATION, name: '学生验证', description: '只有学生用户才有此权限' }
]

// 用户类型测试
const userTypes = [
  { key: 'guest', name: '是否为游客' },
  { key: 'adult', name: '是否为成人用户' },
  { key: 'student', name: '是否为学生用户' }
]

// 测试路由
const testRoutes = [
  {
    path: '/',
    name: '首页',
    meta: {}
  },
  {
    path: '/login',
    name: '登录页',
    meta: {}
  },
  {
    path: '/order/create',
    name: '创建订单',
    meta: { 
      requiresAuth: true,
      permissions: [PERMISSIONS.CREATE_ORDER]
    }
  },
  {
    path: '/user/profile',
    name: '个人信息',
    meta: { 
      requiresAuth: true,
      permissions: [PERMISSIONS.VIEW_PROFILE]
    }
  },
  {
    path: '/user/passengers',
    name: '乘客管理',
    meta: { 
      requiresAuth: true,
      permissions: [PERMISSIONS.MANAGE_PASSENGERS]
    }
  },
  {
    path: '/student/discount',
    name: '学生优惠',
    meta: { 
      requiresAuth: true,
      userTypes: ['student'],
      permissions: [PERMISSIONS.STUDENT_DISCOUNT]
    }
  }
]

// 权限检查函数
const hasPermissionTest = (permission) => {
  return hasPermission(permission, user.value)
}

const hasUserTypeTest = (type) => {
  return hasUserType(type, user.value)
}

const canAccessRouteTest = (route) => {
  return canAccessRoute(route, user.value)
}

// 当前用户权限
const currentUserPermissions = computed(() => {
  return getUserPermissions(user.value)
})

// 初始化为游客模式
switchUserType('guest')
</script>

<style scoped>
.permission-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #1890ff;
  margin-bottom: 10px;
}

.description {
  color: #666;
  font-size: 16px;
}

.user-status, .user-type-switcher, .permission-tests, .user-type-tests, .route-tests, .directive-tests, .permission-details {
  margin-bottom: 30px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.status-card {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-item label {
  font-weight: bold;
  color: #333;
}

.status-success {
  color: #52c41a;
  font-weight: bold;
}

.status-error {
  color: #ff4d4f;
  font-weight: bold;
}

.user-type-guest {
  color: #666;
}

.user-type-adult {
  color: #1890ff;
}

.user-type-student {
  color: #722ed1;
}

.switcher-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  border-color: #1890ff;
  color: #1890ff;
}

.btn.active {
  background: #1890ff;
  color: #fff;
  border-color: #1890ff;
}

.btn-guest.active {
  background: #666;
  border-color: #666;
}

.btn-student.active {
  background: #722ed1;
  border-color: #722ed1;
}

.test-grid, .type-test-grid, .route-test-grid, .directive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.test-card, .type-test-card, .route-test-card, .directive-card {
  padding: 15px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  background: #fafafa;
}

.test-card h3, .type-test-card h3, .route-test-card h3, .directive-card h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.permission-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.permission-result, .type-result, .route-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.permission-key {
  font-family: monospace;
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
}

.result-success {
  color: #52c41a;
  font-weight: bold;
}

.result-error {
  color: #ff4d4f;
  font-weight: bold;
}

.route-path {
  font-family: monospace;
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.route-meta {
  margin-bottom: 10px;
}

.meta-tag {
  display: inline-block;
  background: #e6f7ff;
  color: #1890ff;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-right: 5px;
  margin-bottom: 5px;
}

.permission-content {
  padding: 10px;
  border-radius: 4px;
  margin-top: 10px;
}

.permission-content.success {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #52c41a;
}

.permissions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.permission-badge {
  display: inline-block;
  background: #1890ff;
  color: #fff;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: bold;
}
</style>