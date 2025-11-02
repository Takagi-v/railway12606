<template>
  <div class="env-test">
    <h2>环境变量测试页面</h2>
    <div class="env-info">
      <h3>当前环境配置</h3>
      <table class="env-table">
        <thead>
          <tr>
            <th>配置项</th>
            <th>值</th>
            <th>说明</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>API_BASE_URL</td>
            <td>{{ envConfig.API_BASE_URL }}</td>
            <td>API基础地址</td>
          </tr>
          <tr>
            <td>REQUEST_TIMEOUT</td>
            <td>{{ envConfig.REQUEST_TIMEOUT }}ms</td>
            <td>请求超时时间</td>
          </tr>
          <tr>
            <td>APP_TITLE</td>
            <td>{{ envConfig.APP_TITLE }}</td>
            <td>应用标题</td>
          </tr>
          <tr>
            <td>APP_VERSION</td>
            <td>{{ envConfig.APP_VERSION }}</td>
            <td>应用版本</td>
          </tr>
          <tr>
            <td>NODE_ENV</td>
            <td>{{ envConfig.NODE_ENV }}</td>
            <td>运行环境</td>
          </tr>
          <tr>
            <td>DEBUG</td>
            <td>{{ envConfig.DEBUG ? '开启' : '关闭' }}</td>
            <td>调试模式</td>
          </tr>
          <tr>
            <td>USE_MOCK</td>
            <td>{{ envConfig.USE_MOCK ? '开启' : '关闭' }}</td>
            <td>Mock数据</td>
          </tr>
          <tr>
            <td>UPLOAD_SIZE_LIMIT</td>
            <td>{{ envConfig.UPLOAD_SIZE_LIMIT }}MB</td>
            <td>上传文件大小限制</td>
          </tr>
          <tr>
            <td>PAGE_SIZE</td>
            <td>{{ envConfig.PAGE_SIZE }}</td>
            <td>分页大小</td>
          </tr>
          <tr>
            <td>TOKEN_EXPIRE_HOURS</td>
            <td>{{ envConfig.TOKEN_EXPIRE_HOURS }}小时</td>
            <td>Token过期时间</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="test-actions">
      <h3>功能测试</h3>
      <button @click="testNetworkConnection" class="test-btn">测试网络连接</button>
      <button @click="testApiRequest" class="test-btn">测试API请求</button>
      <button @click="testDebugLog" class="test-btn">测试调试日志</button>
      <div v-if="testResult" class="test-result">
        <h4>测试结果：</h4>
        <pre>{{ testResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ENV_CONFIG, { isDebug, isDev, isProd } from '@/utils/env'
import { getUserProfile } from '@/api/auth'

const envConfig = ENV_CONFIG
const testResult = ref('')

const testApiRequest = async () => {
  try {
    testResult.value = '正在测试API请求...'
    
    // 如果启用了Mock模式，显示Mock测试结果
    if (envConfig.USE_MOCK) {
      testResult.value = `Mock模式测试成功！\n模拟用户数据: {
  "id": 1,
  "username": "test_user",
  "email": "test@example.com",
  "created_at": "${new Date().toISOString()}"
}`
      return
    }
    
    // 真实API测试
    const response = await getUserProfile()
    testResult.value = `API请求测试成功！\n响应数据: ${JSON.stringify(response, null, 2)}`
  } catch (error) {
    testResult.value = `API请求测试失败！\n错误信息: ${error.message}\n\n可能的原因：
1. 后端服务未启动 (检查端口8000)
2. 用户未登录 (需要先登录获取Token)
3. 网络连接问题
4. CORS配置问题

建议：
- 先点击"测试网络连接"检查后端状态
- 或者启用Mock模式进行测试 (设置 VITE_USE_MOCK=true)`
  }
}

const testNetworkConnection = async () => {
  try {
    testResult.value = '正在测试网络连接...'
    
    // 创建一个带超时的fetch请求
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000)
    
    const response = await fetch(`${envConfig.API_BASE_URL.replace('/api', '')}/health`, {
      signal: controller.signal,
      method: 'GET'
    })
    
    clearTimeout(timeoutId)
    
    if (response.ok) {
      const data = await response.json()
      testResult.value = `网络连接测试成功！✅
后端服务状态: ${data.status || 'healthy'}
API地址: ${envConfig.API_BASE_URL}
响应时间: ${Date.now() - performance.now()}ms
状态码: ${response.status}`
    } else {
      testResult.value = `网络连接测试失败！❌
状态码: ${response.status}
API地址: ${envConfig.API_BASE_URL}

可能的问题：
- 后端服务配置错误
- API路径不正确`
    }
  } catch (error) {
    testResult.value = `网络连接测试失败！❌
错误信息: ${error.message}

可能的原因：
1. 后端服务未启动 (端口8000)
2. 防火墙阻止连接
3. 网络配置问题
4. API地址配置错误: ${envConfig.API_BASE_URL}

解决方案：
1. 检查后端服务是否运行: netstat -ano | findstr :8000
2. 启动后端服务: cd backend && run_windows.bat
3. 检查防火墙设置`
  }
}

const testDebugLog = () => {
  console.log('🧪 环境变量测试:', {
    isDev: isDev(),
    isProd: isProd(),
    isDebug: isDebug(),
    config: envConfig
  })
  testResult.value = `调试日志已输出到控制台！\n请打开浏览器开发者工具查看控制台输出。\n\n当前环境: ${envConfig.NODE_ENV}\n调试模式: ${isDebug() ? '开启' : '关闭'}`
}
</script>

<style scoped>
.env-test {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.env-test h2 {
  color: #1890ff;
  margin-bottom: 20px;
}

.env-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}

.env-table th,
.env-table td {
  border: 1px solid #d9d9d9;
  padding: 8px 12px;
  text-align: left;
}

.env-table th {
  background-color: #fafafa;
  font-weight: 600;
}

.test-actions {
  margin-top: 30px;
}

.test-btn {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 10px 20px;
  margin-right: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.test-btn:hover {
  background-color: #40a9ff;
}

.test-result {
  margin-top: 20px;
  padding: 16px;
  background-color: #f6f8fa;
  border: 1px solid #d0d7de;
  border-radius: 6px;
}

.test-result h4 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #24292f;
}

.test-result pre {
  background-color: #ffffff;
  border: 1px solid #d0d7de;
  border-radius: 4px;
  padding: 12px;
  margin: 0;
  overflow-x: auto;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.4;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>