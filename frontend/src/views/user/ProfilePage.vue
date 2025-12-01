<template>
  <div class="profile-page">
    <div class="center-welcome">
      <div class="welcome_data">
        <div class="welcome-tit">
          <img src="@/assets/12306-icons/noticepic.png" alt="" class="welcome-notice">
          <strong class="welcome-name">{{ displayName }}</strong>
          <span>{{ greetingSuffix }}</span>
        </div>
        <div class="welcome-con">
          <p>
            欢迎您登录中国铁路客户服务中心网站。<br>
            <span style="color: red;">如果您的密码在其他网站也使用，建议您修改本网站密码。</span><br>
            如果您要接收12306的服务邮件，请<a href="javascript:;" class="txt-primary underline">验证邮箱</a>。<br>
            如果您需要预订车票，请您点击<a href="javascript:;" @click.prevent="go('/leftTicket/single')" class="txt-primary underline">车票预订</a>。
          </p>
        </div>
      </div>
      <ul class="welcome-code">
        <li id="weixinImg">
          <div class="code-pic">
            <img src="@/assets/12306-icons/wechat-qr.png" title="使用微信扫一扫，可通过微信公众号接收12306行程通知" alt="WeChat QR">
          </div>
          <div class="code-txt">
            使用微信扫一扫，可通过<br>微信公众号接收12306行程通知
          </div>
        </li>
        <li id="aliImg">
          <div class="code-pic">
            <img src="@/assets/12306-icons/alipay-qr.png" title="使用支付宝扫一扫，可通过支付宝通知提醒接收12306行程通知" alt="Alipay QR">
          </div>
          <div class="code-txt">
            使用支付宝扫一扫，可通过<br>支付宝通知提醒接收12306行程通知
          </div>
        </li>
      </ul>
      <div class="tips-box">
        <h2>温馨提示：</h2>
        <p>
          1.消息通知方式进行相关调整，将通过“铁路12306”App客户端为您推送相关消息（需开启通知权限）。您也可以扫描关注“铁路12306”微信公众号或支付宝生活号，选择通过微信或支付宝接收。列车运行调整的通知仍然发送短信通知给您。
        </p>
        <p>
          2.您可通过“账号安全”中的<a class="index_notice" href="javascript:;" style="color: #0077ff">“通知设置”</a>修改您接收信息服务的方式。
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = useRouter()
const go = path => router.push(path)

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const displayName = computed(() => {
  const u = user.value || {}
  return u.nickname || u.username || u.name || '用户'
})
const greetingSuffix = computed(() => {
  const h = new Date().getHours()
  if (h < 11) return '先生,上午好！'
  if (h < 13) return '先生,中午好！'
  if (h < 18) return '先生,下午好！'
  return '先生,晚上好！'
})
</script>

<style scoped>
.profile-page {
  width: 100%;
}

.center-welcome {
  padding: 20px 30px 30px;
  background: #fafdff;
  min-height: 842px;
  box-sizing: border-box;
  margin: -16px;
  width: calc(100% + 32px);
  color: #333;
}

.welcome-tit {
  height: 65px;
  line-height: 65px;
  font-size: 18px;
  display: flex;
  align-items: center;
}

.welcome-notice {
  margin-right: 10px;
  vertical-align: middle;
}

.welcome-name {
  margin-right: 5px;
  font-weight: bold;
}

.welcome-con {
  padding: 10px 20px;
  margin-top: 15px;
  border: 1px dashed #9eccfe;
  background: #fafdff;
  line-height: 32px;
  font-size: 14px;
}

.welcome-con p {
  margin: 0;
}

.txt-primary {
  color: #0077ff;
  text-decoration: none;
}

.txt-primary.underline:hover {
  text-decoration: underline;
}

.welcome-code {
  display: flex;
  margin: 40px 0 30px;
  padding: 0;
  list-style: none;
  gap: 60px;
}

.welcome-code li {
  display: flex;
  align-items: center;
  gap: 15px;
}

.code-pic img {
  width: 120px;
  height: 120px;
  border: 1px solid #eee;
}

.code-txt {
  line-height: 24px;
  font-size: 14px;
  color: #666;
}

.tips-box {
  padding: 10px 20px;
  border: 2px solid #ffddba;
  background: #fffbf8;
  font-size: 14px;
  line-height: 24px;
}

.tips-box h2 {
  margin: 0 0 10px;
  font-size: 14px;
  font-weight: bold;
  color: #333;
}

.tips-box p {
  margin: 0 0 5px;
  text-indent: 2em;
}

.index_notice {
  color: #0077ff;
  text-decoration: none;
}

.index_notice:hover {
  text-decoration: underline;
}
</style>
