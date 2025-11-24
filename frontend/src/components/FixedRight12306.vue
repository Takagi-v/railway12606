<template>
  <div v-if="visible" class="fixed-right">
    <ul class="fixed-right-menu">
      <li class="menu-item">
        <a href="javascript:;" class="menu-hd" @click.prevent="goNotice">
          <i class="icon icon-notice"></i>
          <h4 class="menu-name">最新发布</h4>
        </a>
      </li>
      <li class="menu-item">
        <a href="javascript:;" class="menu-hd" @click.prevent="goServiceNumber">
          <i class="icon icon-phone"></i>
          <h4 class="menu-name">联系客服</h4>
        </a>
      </li>
      <li class="menu-item menu-item--hoverable">
        <a href="javascript:;" class="menu-hd">
          <i class="icon icon-code"></i>
          <h4 class="menu-name">APP下载</h4>
        </a>
        <div class="menu-bd menu-code">
          <h4 class="menu-code-name">铁路12306</h4>
          <div class="menu-code-pic">
            <img :src="downloadImage" alt="铁路12306 APP 下载二维码" />
            <div class="code-tips">
              官方APP下载，目前铁路未授权其他网站或APP开展类似服务内容，敬请广大用户注意。
            </div>
          </div>
        </div>
      </li>
      <li class="menu-item" id="close-right">
        <a href="javascript:;" class="menu-hd" @click.prevent="visible = false">
          <i class="icon icon-close"></i>
          <h4 class="menu-name">关闭</h4>
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const visible = ref(true)

// 使用项目现有本地资源（frontend/pics）
const downloadImage = new URL('../../pics/download.png', import.meta.url).href

const goNotice = () => {
  // 如有“最新发布/公告”路由则跳转，否则先留在首页
  router.push({ path: '/' })
}
const goServiceNumber = () => {
  // 可指向站内“联系客服/服务热线”页面或弹框，先占位
  router.push({ path: '/' })
}
</script>

<style scoped>
.fixed-right {
  position: fixed;
  right: 0;
  top: 50%;
  margin-top: -170px; /* 与官网一致，大致垂直居中 */
  z-index: 1100;
}

.fixed-right-menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.menu-item {
  width: 110px;
  background: #efefef; /* 贴近官网浅灰底 */
  border: 1px solid #ddd;
  border-right: none;
  margin-bottom: 6px;
  box-shadow: none;
}

.menu-hd {
  text-align: center;
  display: block;
  padding: 10px 8px;
  color: #666;
  text-decoration: none;
}
.menu-hd:hover {
  color: #3b99fc;
}

.menu-name {
  margin: 4px 0 0;
  font-size: 14px;
  font-weight: 500;
}

/* 使用官网 iconfont 渲染图标 */
.menu-hd .icon {
  display: block;
  margin: 0 auto 4px;
  font-size: 22px;
  line-height: 1;
  color: #666; /* 官网图标为中性灰 */
  background: transparent; /* 防止出现色块背景 */
}
.menu-hd:hover .icon {
  color: #3b99fc;
}

/* APP下载 - 二维码面板（hover显示） */
.menu-item--hoverable {
  position: relative;
}
.menu-code {
  position: absolute;
  left: -260px; /* 面板在按钮左侧展开 */
  top: 0;
  width: 240px;
  padding: 12px;
  background: #fff;
  border: 1px solid #e5e5e5;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  visibility: hidden;
  opacity: 0;
  transform: translateX(8px);
  transition: 0.25s ease-in-out;
}
.menu-item--hoverable:hover .menu-code {
  visibility: visible;
  opacity: 1;
  transform: translateX(0);
}
.menu-code-name {
  margin: 0 0 8px;
  font-size: 14px;
  color: #333;
}
.menu-code-pic {
  display: block;
  width: 100%;
  position: relative;
}
.menu-code-pic img {
  width: 100%;
  height: auto;
  display: block;
}
.code-tips {
  margin-top: 8px;
  font-size: 12px;
  color: #888;
  line-height: 1.4;
}

/* 关闭按钮样式：与其他项一致（灰色，hover 蓝色），不做额外覆盖 */
</style>
