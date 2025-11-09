<template>
  <div class="train-management">
    <div class="page-header">
      <h1>车次管理</h1>
      <p>管理系统中的所有车次信息</p>
    </div>

    <div class="management-content">
      <div class="content-card">
        <h2>车次列表</h2>
        <p>这里将显示车次列表和管理功能</p>
        
        <!-- 权限测试区域 -->
        <div class="permission-test">
          <h3>权限测试</h3>
          
          <PermissionWrapper :permissions="['train:create']">
            <button class="btn btn-primary">创建车次 (需要 train:create 权限)</button>
          </PermissionWrapper>
          
          <PermissionWrapper :permissions="['train:delete']">
            <button class="btn btn-danger">删除车次 (需要 train:delete 权限)</button>
          </PermissionWrapper>
          
          <button v-permission="'train:update'" class="btn btn-secondary">
            编辑车次 (需要 train:update 权限)
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
.train-management {
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
  border-left: 4px solid #17a2b8;
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

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>