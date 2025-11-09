<template>
  <div class="system-settings">
    <div class="page-header">
      <h1>系统设置</h1>
      <p>管理系统配置和设置</p>
    </div>

    <div class="management-content">
      <div class="content-card">
        <h2>系统配置</h2>
        <p>这里将显示系统设置和配置选项</p>
        
        <!-- 权限测试区域 -->
        <div class="permission-test">
          <h3>权限测试</h3>
          
          <PermissionWrapper :permissions="['system:manage']">
            <button class="btn btn-primary">系统管理 (需要 system:manage 权限)</button>
          </PermissionWrapper>
          
          <PermissionWrapper :permissions="['system:admin']">
            <button class="btn btn-danger">系统管理员 (需要 system:admin 权限)</button>
          </PermissionWrapper>
          
          <button v-role="'super_admin'" class="btn btn-warning">
            超级管理员功能 (需要 super_admin 角色)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import PermissionWrapper from '@/components/PermissionWrapper.vue'
</script>

<style scoped>
.system-settings {
  padding: 2rem;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
}

.management-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.content-card h2 {
  color: #333;
  margin-bottom: 1rem;
}

.permission-test {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #6f42c1;
}

.permission-test h3 {
  color: #333;
  margin-bottom: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>