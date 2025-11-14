<template>
  <div v-if="hasAccess" :class="wrapperClass">
    <slot />
  </div>
  <div v-else-if="showFallback" :class="fallbackClass">
    <slot name="fallback">
      <div class="permission-denied">
        <i class="icon-lock"></i>
        <span>{{ fallbackMessage }}</span>
      </div>
    </slot>
  </div>
</template>

<script>
import { computed, defineComponent } from "vue";
import { usePermissionStore } from "@/stores/permission";
import { useUserStore } from "@/stores/user";

export default defineComponent({
  name: "PermissionWrapper",
  props: {
    // 所需权限
    permissions: {
      type: [String, Array],
      default: null,
    },
    // 所需角色
    roles: {
      type: [String, Array],
      default: null,
    },
    // 权限检查模式：'any' 或 'all'
    permissionMode: {
      type: String,
      default: "any",
      validator: (value) => ["any", "all"].includes(value),
    },
    // 角色检查模式：'any' 或 'all'
    roleMode: {
      type: String,
      default: "any",
      validator: (value) => ["any", "all"].includes(value),
    },
    // 是否显示无权限时的后备内容
    showFallback: {
      type: Boolean,
      default: false,
    },
    // 无权限时的提示信息
    fallbackMessage: {
      type: String,
      default: "您没有权限访问此内容",
    },
    // 包装器样式类
    wrapperClass: {
      type: String,
      default: "",
    },
    // 后备内容样式类
    fallbackClass: {
      type: String,
      default: "permission-fallback",
    },
    // 是否需要登录
    requireAuth: {
      type: Boolean,
      default: true,
    },
  },
  setup(props) {
    const permissionStore = usePermissionStore();
    const userStore = useUserStore();

    // 检查是否有访问权限
    const hasAccess = computed(() => {
      // 如果需要登录但用户未登录
      if (props.requireAuth && !userStore.isAuthenticated) {
        return false;
      }

      // 如果不需要任何权限或角色，直接允许访问
      if (!props.permissions && !props.roles) {
        return true;
      }

      let hasPermission = true;
      let hasRole = true;

      // 检查权限
      if (props.permissions) {
        if (Array.isArray(props.permissions)) {
          hasPermission =
            props.permissionMode === "all"
              ? permissionStore.hasAllPermissions(props.permissions)
              : permissionStore.hasAnyPermission(props.permissions);
        } else {
          hasPermission = permissionStore.hasPermission(props.permissions);
        }
      }

      // 检查角色
      if (props.roles) {
        if (Array.isArray(props.roles)) {
          hasRole =
            props.roleMode === "all"
              ? permissionStore.hasAllRoles(props.roles)
              : permissionStore.hasAnyRole(props.roles);
        } else {
          hasRole = permissionStore.hasRole(props.roles);
        }
      }

      return hasPermission && hasRole;
    });

    return {
      hasAccess,
    };
  },
});
</script>

<style scoped>
.permission-denied {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #999;
  font-size: 14px;
}

.permission-denied .icon-lock {
  margin-right: 8px;
  font-size: 16px;
}

.permission-fallback {
  background-color: #f5f5f5;
  border: 1px dashed #ddd;
  border-radius: 4px;
  text-align: center;
}
</style>
