import PermissionWrapper from './PermissionWrapper.vue'
import PermissionButton from './PermissionButton.vue'

// 导出组件
export {
  PermissionWrapper,
  PermissionButton
}

// 安装插件
export default {
  install(app) {
    app.component('PermissionWrapper', PermissionWrapper)
    app.component('PermissionButton', PermissionButton)
  }
}