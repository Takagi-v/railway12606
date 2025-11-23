<template>
  <button
    v-if="shouldShow"
    :class="buttonClass"
    :disabled="isDisabled"
    :type="type"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script>
import { computed, defineComponent } from 'vue'
import { usePermissionStore } from '@/stores/permission'
import { useUserStore } from '@/stores/user'

export default defineComponent({
  name: 'PermissionButton',
  props: {
    // 所需权限
    permissions: {
      type: [String, Array],
      default: null
    },
    // 所需角色
    roles: {
      type: [String, Array],
      default: null
    },
    // 权限检查模式：'any' 或 'all'
    permissionMode: {
      type: String,
      default: 'any',
      validator: value => ['any', 'all'].includes(value)
    },
    // 角色检查模式：'any' 或 'all'
    roleMode: {
      type: String,
      default: 'any',
      validator: value => ['any', 'all'].includes(value)
    },
    // 按钮类型
    type: {
      type: String,
      default: 'button'
    },
    // 无权限时的行为：'hide' 隐藏, 'disable' 禁用
    noPermissionBehavior: {
      type: String,
      default: 'hide',
      validator: value => ['hide', 'disable'].includes(value)
    },
    // 自定义样式类
    customClass: {
      type: String,
      default: ''
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    // 是否需要登录
    requireAuth: {
      type: Boolean,
      default: true
    }
  },
  emits: ['click', 'permission-denied'],
  setup(props, { emit }) {
    const permissionStore = usePermissionStore()
    const userStore = useUserStore()

    // 检查是否有权限
    const hasPermission = computed(() => {
      // 如果需要登录但用户未登录
      if (props.requireAuth && !userStore.isAuthenticated) {
        return false
      }

      // 如果不需要任何权限或角色，直接允许
      if (!props.permissions && !props.roles) {
        return true
      }

      let permissionCheck = true
      let roleCheck = true

      // 检查权限
      if (props.permissions) {
        if (Array.isArray(props.permissions)) {
          permissionCheck =
            props.permissionMode === 'all'
              ? permissionStore.hasAllPermissions(props.permissions)
              : permissionStore.hasAnyPermission(props.permissions)
        } else {
          permissionCheck = permissionStore.hasPermission(props.permissions)
        }
      }

      // 检查角色
      if (props.roles) {
        if (Array.isArray(props.roles)) {
          roleCheck =
            props.roleMode === 'all'
              ? permissionStore.hasAllRoles(props.roles)
              : permissionStore.hasAnyRole(props.roles)
        } else {
          roleCheck = permissionStore.hasRole(props.roles)
        }
      }

      return permissionCheck && roleCheck
    })

    // 是否应该显示按钮
    const shouldShow = computed(() => {
      return hasPermission.value || props.noPermissionBehavior === 'disable'
    })

    // 是否禁用按钮
    const isDisabled = computed(() => {
      return props.disabled || (!hasPermission.value && props.noPermissionBehavior === 'disable')
    })

    // 按钮样式类
    const buttonClass = computed(() => {
      const classes = ['permission-button']

      if (props.customClass) {
        classes.push(props.customClass)
      }

      if (!hasPermission.value) {
        classes.push('permission-denied')
      }

      if (isDisabled.value) {
        classes.push('disabled')
      }

      return classes.join(' ')
    })

    // 处理点击事件
    const handleClick = event => {
      if (!hasPermission.value) {
        emit('permission-denied', {
          permissions: props.permissions,
          roles: props.roles,
          event
        })
        return
      }

      emit('click', event)
    }

    return {
      shouldShow,
      isDisabled,
      buttonClass,
      handleClick
    }
  }
})
</script>

<style scoped>
.permission-button {
  cursor: pointer;
  transition: all 0.3s ease;
}

.permission-button.disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.permission-button.permission-denied {
  background-color: #f5f5f5;
  color: #999;
  border-color: #ddd;
}

.permission-button.permission-denied:hover {
  background-color: #f5f5f5;
  color: #999;
  border-color: #ddd;
}
</style>
