<template>
  <div class="permission-test">
    <a-card title="权限系统测试页面" style="margin: 20px">
      <!-- 用户信息 -->
      <a-card type="inner" title="用户信息" style="margin-bottom: 16px">
        <a-descriptions :column="2">
          <a-descriptions-item label="用户名">{{
            userStore.user?.username || "未登录"
          }}</a-descriptions-item>
          <a-descriptions-item label="邮箱">{{
            userStore.user?.email || "-"
          }}</a-descriptions-item>
          <a-descriptions-item label="登录状态">
            <a-tag :color="userStore.isAuthenticated ? 'green' : 'red'">
              {{ userStore.isAuthenticated ? "已登录" : "未登录" }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="用户角色">
            <a-tag
              v-for="role in permissionStore.userRoles"
              :key="role"
              color="blue"
            >
              {{ role }}
            </a-tag>
            <span v-if="!permissionStore.userRoles.length">无角色</span>
          </a-descriptions-item>
        </a-descriptions>
      </a-card>

      <!-- 权限测试 -->
      <a-card type="inner" title="权限控制测试" style="margin-bottom: 16px">
        <a-row :gutter="16">
          <a-col :span="12">
            <h4>组件权限测试</h4>

            <!-- 权限包装器测试 -->
            <PermissionWrapper permissions="user:read">
              <a-alert
                message="您有用户读取权限"
                type="success"
                style="margin-bottom: 8px"
              />
            </PermissionWrapper>

            <PermissionWrapper permissions="user:write">
              <a-alert
                message="您有用户写入权限"
                type="info"
                style="margin-bottom: 8px"
              />
            </PermissionWrapper>

            <PermissionWrapper permissions="admin:system">
              <a-alert
                message="您有系统管理权限"
                type="warning"
                style="margin-bottom: 8px"
              />
            </PermissionWrapper>

            <!-- 权限按钮测试 -->
            <div style="margin-top: 16px">
              <PermissionButton
                permissions="user:read"
                type="primary"
                style="margin-right: 8px"
                @click="handleClick('用户读取')"
              >
                用户读取按钮
              </PermissionButton>

              <PermissionButton
                permissions="user:write"
                type="default"
                style="margin-right: 8px"
                @click="handleClick('用户写入')"
              >
                用户写入按钮
              </PermissionButton>

              <PermissionButton
                permissions="admin:system"
                type="danger"
                @click="handleClick('系统管理')"
              >
                系统管理按钮
              </PermissionButton>
            </div>
          </a-col>

          <a-col :span="12">
            <h4>指令权限测试</h4>

            <!-- 权限指令测试 -->
            <div v-permission="'user:read'" style="margin-bottom: 8px">
              <a-tag color="green">v-permission="user:read" - 显示</a-tag>
            </div>

            <div v-permission="'user:write'" style="margin-bottom: 8px">
              <a-tag color="blue">v-permission="user:write" - 显示</a-tag>
            </div>

            <div v-permission="'admin:system'" style="margin-bottom: 8px">
              <a-tag color="red">v-permission="admin:system" - 显示</a-tag>
            </div>

            <!-- 角色指令测试 -->
            <div v-role="'admin'" style="margin-bottom: 8px">
              <a-tag color="purple">v-role="admin" - 显示</a-tag>
            </div>

            <div v-role="'super_admin'" style="margin-bottom: 8px">
              <a-tag color="orange">v-role="super_admin" - 显示</a-tag>
            </div>

            <!-- 复合权限测试 -->
            <div
              v-auth="{ permissions: ['user:read', 'user:write'], mode: 'any' }"
              style="margin-bottom: 8px"
            >
              <a-tag color="cyan">v-auth (any user permissions) - 显示</a-tag>
            </div>

            <div
              v-auth="{ permissions: ['user:read', 'user:write'], mode: 'all' }"
              style="margin-bottom: 8px"
            >
              <a-tag color="lime">v-auth (all user permissions) - 显示</a-tag>
            </div>
          </a-col>
        </a-row>
      </a-card>

      <!-- 权限检查工具 -->
      <a-card type="inner" title="权限检查工具">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form layout="vertical">
              <a-form-item label="检查权限">
                <a-input
                  v-model:value="testPermission"
                  placeholder="输入权限代码，如: user:read"
                  @press-enter="checkPermission"
                />
                <a-button
                  type="primary"
                  style="margin-top: 8px"
                  @click="checkPermission"
                >
                  检查权限
                </a-button>
              </a-form-item>
            </a-form>
          </a-col>

          <a-col :span="12">
            <a-form layout="vertical">
              <a-form-item label="检查角色">
                <a-input
                  v-model:value="testRole"
                  placeholder="输入角色名称，如: admin"
                  @press-enter="checkRole"
                />
                <a-button
                  type="primary"
                  style="margin-top: 8px"
                  @click="checkRole"
                >
                  检查角色
                </a-button>
              </a-form-item>
            </a-form>
          </a-col>
        </a-row>

        <!-- 检查结果 -->
        <div v-if="checkResults.length" style="margin-top: 16px">
          <h4>检查结果：</h4>
          <a-list :data-source="checkResults" size="small">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-tag :color="item.result ? 'green' : 'red'">
                  {{ item.type }}: {{ item.value }} -
                  {{ item.result ? "有权限" : "无权限" }}
                </a-tag>
              </a-list-item>
            </template>
          </a-list>
        </div>
      </a-card>

      <!-- 当前权限列表 -->
      <a-card type="inner" title="当前用户权限">
        <a-row :gutter="16">
          <a-col :span="12">
            <h4>用户权限</h4>
            <a-tag
              v-for="permission in permissionStore.userPermissions"
              :key="permission"
              color="blue"
              style="margin-bottom: 4px"
            >
              {{ permission }}
            </a-tag>
            <div
              v-if="!permissionStore.userPermissions.length"
              style="color: #999"
            >
              暂无权限
            </div>
          </a-col>

          <a-col :span="12">
            <h4>用户角色</h4>
            <a-tag
              v-for="role in permissionStore.userRoles"
              :key="role"
              color="green"
              style="margin-bottom: 4px"
            >
              {{ role }}
            </a-tag>
            <div v-if="!permissionStore.userRoles.length" style="color: #999">
              暂无角色
            </div>
          </a-col>
        </a-row>
      </a-card>
    </a-card>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { usePermissionStore } from "@/stores/permission";
import { message } from "ant-design-vue";

export default {
  name: "PermissionTest",
  setup() {
    const userStore = useUserStore();
    const permissionStore = usePermissionStore();

    const testPermission = ref("");
    const testRole = ref("");
    const checkResults = ref([]);

    const handleClick = (action) => {
      message.success(`${action}按钮被点击`);
    };

    const checkPermission = () => {
      if (!testPermission.value.trim()) {
        message.warning("请输入权限代码");
        return;
      }

      const result = permissionStore.hasPermission(testPermission.value.trim());
      checkResults.value.unshift({
        type: "权限",
        value: testPermission.value.trim(),
        result,
      });

      // 限制结果数量
      if (checkResults.value.length > 10) {
        checkResults.value = checkResults.value.slice(0, 10);
      }

      testPermission.value = "";
    };

    const checkRole = () => {
      if (!testRole.value.trim()) {
        message.warning("请输入角色名称");
        return;
      }

      const result = permissionStore.hasRole(testRole.value.trim());
      checkResults.value.unshift({
        type: "角色",
        value: testRole.value.trim(),
        result,
      });

      // 限制结果数量
      if (checkResults.value.length > 10) {
        checkResults.value = checkResults.value.slice(0, 10);
      }

      testRole.value = "";
    };

    onMounted(async () => {
      // 确保权限数据已加载
      if (userStore.isAuthenticated && userStore.user) {
        await permissionStore.loadUserPermissions(userStore.user.id);
      }
    });

    return {
      userStore,
      permissionStore,
      testPermission,
      testRole,
      checkResults,
      handleClick,
      checkPermission,
      checkRole,
    };
  },
};
</script>

<style scoped>
.permission-test {
  min-height: 100vh;
  background-color: #f0f2f5;
}

.ant-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}
</style>
