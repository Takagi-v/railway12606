<template>
  <div class="profile-page">
    <div v-if="activeSection === 'view'" class="center-form-item" id="js-minHeight">
      <!-- 基本信息 -->
      <div class="center-tit">
        <div class="tit-name">基本信息</div>
        <div class="pull-right">
          <a href="javascript:;" class="btn btn-default btn-edit" v-if="!isEditingBasic" @click="startEdit('basic')">编辑</a>
          <template v-else>
             <a href="javascript:;" class="btn btn-primary btn-save" :class="{ disabled: editLoading }" @click="saveEdit('basic')">保存</a>
             <a href="javascript:;" class="btn btn-default btn-cancel" @click="cancelEdit('basic')" style="margin-left: 10px;">取消</a>
          </template>
        </div>
      </div>
      <!-- 显示 -->
      <div v-if="!isEditingBasic && user" class="form-list form-list-view" id="basic_info_view">
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>用户名：</div>
          <div class="form-bd"><div class="form-bd-txt">{{ user.username }}</div></div>
        </div>
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>姓名：</div>
          <div class="form-bd"><div class="form-bd-txt">{{ user.real_name || user.name }}</div></div>
        </div>
        <div class="form-item">
          <div class="form-label">国家/地区：</div>
          <div class="form-bd"><div class="form-bd-txt">中国China</div></div>
        </div>
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>证件类型：</div>
          <div class="form-bd"><div class="form-bd-txt" data-val="1">居民身份证</div></div>
        </div>
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>证件号码：</div>
          <div class="form-bd"><div class="form-bd-txt">{{ maskIdNo(user.id_number || user.id_no) }}</div></div>
        </div>
        <div class="form-item">
          <div class="form-label">核验状态：</div>
          <div class="form-bd">
            <div class="form-bd-txt">
              <span class="txt-second succ-color">已通过</span>
            </div>
          </div>
        </div>
      </div>
      <!-- 编辑 -->
      <div v-else-if="isEditingBasic && user" class="form-list form-list-edit">
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>用户名：</div>
          <div class="form-bd"><div class="form-bd-txt">{{ user.username }}</div></div>
        </div>
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>姓名：</div>
          <div class="form-bd"><input type="text" class="input input-railway" v-model="editForm.real_name" style="width: 200px;" /></div>
        </div>
        <div class="form-item">
          <div class="form-label">国家/地区：</div>
          <div class="form-bd"><div class="form-bd-txt">中国China</div></div>
        </div>
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>证件类型：</div>
          <div class="form-bd"><div class="form-bd-txt">居民身份证</div></div>
        </div>
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>证件号码：</div>
          <div class="form-bd"><div class="form-bd-txt">{{ maskIdNo(user.id_number || user.id_no) }}</div></div>
        </div>
      </div>

      <div class="line-dashed"></div>
      
      <!-- 联系方式 -->
      <div class="center-tit">
        <div class="tit-name">联系方式</div>
        <div class="pull-right">
          <a href="javascript:;" class="btn btn-default btn-edit" v-if="!isEditingContact" @click="startEdit('contact')">编辑</a>
          <template v-else>
             <a href="javascript:;" class="btn btn-primary btn-save" :class="{ disabled: editLoading }" @click="saveEdit('contact')">保存</a>
             <a href="javascript:;" class="btn btn-default btn-cancel" @click="cancelEdit('contact')" style="margin-left: 10px;">取消</a>
          </template>
        </div>
      </div>
      <!-- 显示 -->
      <div v-if="!isEditingContact && user" class="form-list form-list-view" id="relation_way_view">
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>手机号：</div>
          <div class="form-bd">
            <div class="form-bd-txt">
              (+86) {{ maskMobile(user.phone || user.mobile) }}
            </div>
            <div class="tips one-line txt-second succ-color" style="margin-left:5px; display:inline-block;">已通过核验</div>
          </div>
        </div>
        <div class="form-item">
          <div class="form-label">邮箱：</div>
          <div class="form-bd"><div class="form-bd-txt">{{ user.email || '' }}</div></div>
        </div>
      </div>
      <!-- 编辑 -->
      <div v-else-if="isEditingContact && user" class="form-list form-list-edit">
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>手机号：</div>
          <div class="form-bd">
            <input type="text" class="input input-railway" v-model="editForm.phone" style="width: 200px;" />
            <div class="tips one-line txt-second" style="margin-left:10px; display:inline-block; font-size:12px;">(修改后需重新核验)</div>
          </div>
        </div>
        <div class="form-item">
          <div class="form-label">邮箱：</div>
          <div class="form-bd">
            <input type="email" class="input input-railway" v-model="editForm.email" style="width: 200px;" />
          </div>
        </div>
      </div>

      <div class="line-dashed"></div>

      <!-- 附加信息 -->
      <div class="center-tit">
        <div class="tit-name">附加信息</div>
        <div class="pull-right">
          <a href="javascript:;" class="btn btn-default btn-edit" v-if="!isEditingAppend" @click="startEdit('append')">编辑</a>
          <template v-else>
             <a href="javascript:;" class="btn btn-primary btn-save" :class="{ disabled: editLoading }" @click="saveEdit('append')">保存</a>
             <a href="javascript:;" class="btn btn-default btn-cancel" @click="cancelEdit('append')" style="margin-left: 10px;">取消</a>
          </template>
        </div>
      </div>
      <!-- 显示 -->
      <div v-if="!isEditingAppend && user" class="form-list form-list-view" id="append_info_view">
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>优惠(待)类型：</div>
          <div class="form-bd"><div class="form-bd-txt" id="isStudent">{{ getUserTypeLabel(user.user_type) }}</div></div>
        </div>
      </div>
      <!-- 编辑 -->
      <div v-else-if="isEditingAppend && user" class="form-list form-list-edit">
        <div class="form-item">
          <div class="form-label"><span class="required">*</span>优惠(待)类型：</div>
          <div class="form-bd">
              <select class="input input-railway" v-model="editForm.passenger_type" style="width: 200px; height: 30px;">
                <option value="1">成人</option>
                <option value="3">学生</option>
              </select>
            </div>
        </div>
      </div>
    </div>

    <!-- Default Welcome Section -->
    <div v-else class="center-welcome">
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
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = useRouter()
const route = useRoute()
const go = path => router.push(path)

const userStore = useUserStore()
const { user } = storeToRefs(userStore)

const activeSection = computed(() => route.query.section || 'welcome')

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

const maskIdNo = (id) => {
  if (!id || id.length < 10) return id
  return id.substring(0, 4) + '***********' + id.substring(id.length - 3)
}

const maskMobile = (mobile) => {
  if (!mobile || mobile.length < 7) return mobile
  return mobile.substring(0, 3) + '****' + mobile.substring(mobile.length - 4)
}

const getUserTypeLabel = (type) => {
  return type || '成人'
}

// Edit Logic
import { reactive, ref } from 'vue'
import { updateUserProfile } from '@/api/auth'
import { message } from 'ant-design-vue'

const isEditingBasic = ref(false)
const isEditingContact = ref(false)
const isEditingAppend = ref(false)
const editLoading = ref(false)

const editForm = reactive({
  real_name: '',
  email: '',
  phone: '',
  passenger_type: '1' // 1: Adult
})

const startEdit = (section) => {
  if (!user.value) return
  if (section === 'basic') {
    editForm.real_name = user.value.real_name || user.value.name
    isEditingBasic.value = true
  } else if (section === 'contact') {
    editForm.email = user.value.email || ''
    editForm.phone = user.value.phone || user.value.mobile || ''
    isEditingContact.value = true
  } else if (section === 'append') {
    const typeMap = {
      '成人': '1',
      '学生': '3'
    }
    editForm.passenger_type = typeMap[user.value.user_type] || '1'
    isEditingAppend.value = true
  }
}

const cancelEdit = (section) => {
  if (section === 'basic') isEditingBasic.value = false
  if (section === 'contact') isEditingContact.value = false
  if (section === 'append') isEditingAppend.value = false
}

const saveEdit = async (section) => {
  if (!user.value) return
  editLoading.value = true
  try {
    const data = {}
    if (section === 'basic') {
      data.real_name = editForm.real_name
    } else if (section === 'contact') {
      data.email = editForm.email
      // Phone usually requires SMS verification, so we might skip sending it here 
      // or send it if backend allows direct update (backend does allow it now based on code)
      data.phone = editForm.phone
    } else if (section === 'append') {
       // Map dropdown values to backend UserType enum values
       const typeMap = {
         '1': '成人',
         '3': '学生'
       }
       data.user_type = typeMap[editForm.passenger_type]
    }

    const res = await updateUserProfile(data)
    if (res.code === 200) {
      message.success('保存成功')
      await userStore.fetchUserProfile() // Refresh data
      if (section === 'basic') isEditingBasic.value = false
      if (section === 'contact') isEditingContact.value = false
      if (section === 'append') isEditingAppend.value = false
    } else {
      message.error(res.message || '保存失败')
    }
  } catch (err) {
    message.error(err.message || '保存失败')
  } finally {
    editLoading.value = false
  }
}
</script>

<style scoped>
.profile-page {
  width: 100%;
}

/* Original Welcome Styles */
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

/* New Personal Info Styles */
.center-form-item {
  padding: 0;
  width: 100%;
}

.center-tit {
  padding: 10px 0;
  margin-bottom: 20px;
  border-bottom: 2px solid #dedede;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tit-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.pull-right {
  float: right;
}

.form-list {
  margin-bottom: 20px;
}

.form-item {
  display: flex;
  margin-bottom: 20px;
  line-height: 30px;
  font-size: 14px;
  color: #333;
}

.form-label {
  width: 120px;
  text-align: right;
  margin-right: 10px;
  color: #666;
}

.required {
  color: #ff5500;
  margin-right: 4px;
  font-family: Lucida Console, Monaco, Consolas, Courier New, Courier, monospace;
}

.form-bd {
  flex: 1;
  display: flex;
  align-items: center;
}

.form-bd-txt {
  color: #333;
  font-size: 14px;
}

.txt-second {
  color: #999;
}

.succ-color {
  color: #ff9900;
}

.line-dashed {
  border-top: 1px dashed #dedede;
  margin: 20px 0 30px;
}

.btn {
  display: inline-block;
  text-align: center;
  vertical-align: middle;
  cursor: pointer;
  border: 1px solid transparent;
  white-space: nowrap;
  padding: 0 15px;
  font-size: 14px;
  line-height: 28px;
  border-radius: 4px;
  user-select: none;
  text-decoration: none;
}

.btn-default {
  color: #333;
  background-color: #fff;
  border-color: #dedede;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn-default:hover {
  background-color: #f7f7f7;
  border-color: #c6c6c6;
}

.btn-primary {
  color: #fff;
  background-color: #ff9900;
  border-color: #ff9900;
}

.btn-primary:hover {
  background-color: #ffb340;
  border-color: #ffb340;
}

.btn.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  pointer-events: none;
}

.input {
  display: inline-block;
  height: 30px;
  line-height: 30px;
  padding: 0 8px;
  border: 1px solid #dedede;
  border-radius: 4px;
  color: #333;
  outline: none;
  font-size: 14px;
  transition: all 0.2s;
}

.input:focus {
  border-color: #3b99fc;
  box-shadow: 0 0 0 2px rgba(59, 153, 252, 0.2);
}
</style>
