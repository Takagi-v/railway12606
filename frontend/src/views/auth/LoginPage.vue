<template>
  <div class="login-page">
    <!-- 顶栏 Header -->
    <header class="login-header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo">
            <img :src="logoImage" alt="中国铁路12306" class="logo-image" />
            <span class="logo-welcome">欢迎登录 12306</span>
          </div>
        </div>
      </div>
    </header>

    <!-- 主体区域 Main Section -->
    <main class="login-main">
      <div class="bg-slider">
        <div
          class="bg-track"
          :style="{
            width: `${bgImages.length * 100}%`,
            transform: `translateX(-${(currentSlide / bgImages.length) * 100}%)`,
          }"
        >
          <div
            v-for="(img, idx) in bgImages"
            :key="idx"
            class="bg-slide"
            :style="{
              backgroundImage: `url('${img}')`,
              width: `${100 / bgImages.length}%`,
            }"
          ></div>
        </div>
      </div>
      <div class="main-content">
        <div class="promo-section"></div>

        <!-- 右侧登录框 -->
        <div class="login-section">
          <div class="login-card">
            <!-- Tab 切换 -->
            <div class="login-tabs">
              <div
                class="tab-item"
                :class="{ active: activeTab === 'account' }"
                @click="activeTab = 'account'"
              >
                账号登录
              </div>
              <div
                class="tab-item"
                :class="{ active: activeTab === 'qr' }"
                @click="activeTab = 'qr'"
              >
                扫码登录
              </div>
            </div>

            <!-- 账号登录表单 -->
            <div v-if="activeTab === 'account'" class="login-form-container">
              <a-form
                :model="loginForm"
                :rules="rules"
                layout="vertical"
                class="login-form"
                @finish="handleLogin"
              >
                <a-form-item name="username">
                  <a-input
                    v-model:value="loginForm.username"
                    placeholder="用户名/邮箱/手机号"
                    size="large"
                    class="login-input"
                  />
                </a-form-item>

                <a-form-item name="password">
                  <a-input-password
                    v-model:value="loginForm.password"
                    placeholder="密码"
                    size="large"
                    class="login-input"
                  />
                </a-form-item>

                <a-form-item>
                  <a-button
                    type="primary"
                    html-type="submit"
                    size="large"
                    block
                    :loading="loading"
                    class="login-button"
                  >
                    登录
                  </a-button>
                </a-form-item>
              </a-form>

              <div class="login-links">
                <a-button
                  type="link"
                  class="register-link"
                  @click="router.push('/register')"
                >
                  注册新用户
                </a-button>
                <a-button
                  type="link"
                  class="forgot-link"
                  @click="router.push('/forgot-password')"
                >
                  忘记密码？
                </a-button>
              </div>
            </div>

            <!-- 扫码登录 -->
            <div v-else class="qr-login-container">
              <div class="qr-login">
                <div class="qr-code-large">
                  <div class="qr-placeholder-large">
                    <div class="qr-grid-large">
                      <div v-for="i in 64" :key="i" class="qr-dot"></div>
                    </div>
                  </div>
                </div>
                <p class="qr-instruction">请使用12306手机客户端扫码登录</p>
              </div>
            </div>

            <!-- 服务时间提示 -->
            <div class="service-time">
              <p>
                铁路12306每日5:00至次日1:00（周二为5:00至24:00）为您提供服务
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="slider-dots">
        <span
          v-for="(img, idx) in bgImages"
          :key="'dot' + idx"
          class="dot"
          :class="{ active: currentSlide === idx }"
          @click="setSlide(idx)"
        ></span>
      </div>
    </main>

    <LoginFooter />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import LoginFooter from '@/components/LoginFooter.vue'
import { useUserStore } from "@/stores/user";
import { message } from "ant-design-vue";

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

// 响应式数据
const activeTab = ref("account");
const loading = ref(false);
const loginFormRef = ref();
const errorMessage = ref("");
const loginAttempts = ref(0);
const maxAttempts = 5;

const bgImages = [
  new URL("../../../pics/banner-login-20200629.jpg", import.meta.url).href,
  new URL("../../../pics/banner-login-20200924.jpg", import.meta.url).href,
];
const logoImage = new URL("../../../pics/logo@2x.png", import.meta.url).href;
const currentSlide = ref(0);
const setSlide = (i) => {
  currentSlide.value = i;
};

// 验证码相关
const showCaptcha = ref(false);
const captchaImage = ref("");
const captchaToken = ref("");
const captchaLoading = ref(false);

// 二维码登录相关
const qrStatus = ref("loading"); // loading, active, scanned, expired, error
const qrImage = ref("");
const qrToken = ref("");
const qrTimeLeft = ref(120);
const qrTimer = ref(null);
const qrCheckTimer = ref(null);

// 忘记密码相关
const forgotPasswordVisible = ref(false);
const forgotLoading = ref(false);
const forgotCaptchaImage = ref("");
const forgotCaptchaToken = ref("");

// 登录表单数据
const loginForm = reactive({
  username: "",
  password: "",
  captcha: "",
  remember: false,
});

// 忘记密码表单
const forgotForm = reactive({
  identifier: "",
  captcha: "",
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: "请输入用户名/邮箱/手机号", trigger: "blur" },
    {
      validator: (rule, value) => {
        if (!value) return Promise.resolve();

        // 手机号验证
        const phoneRegex = /^1[3-9]\d{9}$/;
        // 用户名验证（字母、数字、下划线，4-20位）
        const usernameRegex = /^[a-zA-Z0-9_]{4,20}$/;
        // 邮箱验证
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (
          !phoneRegex.test(value) &&
          !usernameRegex.test(value) &&
          !emailRegex.test(value)
        ) {
          return Promise.reject("请输入正确的手机号、用户名或邮箱");
        }
        return Promise.resolve();
      },
      trigger: "blur",
    },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, max: 20, message: "密码长度为6-20位", trigger: "blur" },
    {
      validator: (rule, value) => {
        if (!value) return Promise.resolve();

        // 密码强度验证：至少包含字母和数字
        const hasLetter = /[a-zA-Z]/.test(value);
        const hasNumber = /\d/.test(value);

        if (!hasLetter || !hasNumber) {
          return Promise.reject("密码必须包含字母和数字");
        }
        return Promise.resolve();
      },
      trigger: "blur",
    },
  ],
  captcha: [
    {
      required: true,
      message: "请输入验证码",
      trigger: "blur",
      validator: (rule, value) => {
        if (showCaptcha.value && !value) {
          return Promise.reject("请输入验证码");
        }
        if (showCaptcha.value && value && value.length !== 4) {
          return Promise.reject("验证码为4位");
        }
        return Promise.resolve();
      },
    },
  ],
};

// 忘记密码验证规则
const forgotRules = {
  identifier: [
    { required: true, message: "请输入手机号或邮箱", trigger: "blur" },
    {
      validator: (rule, value) => {
        if (!value) return Promise.resolve();

        const phoneRegex = /^1[3-9]\d{9}$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!phoneRegex.test(value) && !emailRegex.test(value)) {
          return Promise.reject("请输入正确的手机号或邮箱");
        }
        return Promise.resolve();
      },
      trigger: "blur",
    },
  ],
  captcha: [{ required: true, message: "请输入验证码", trigger: "blur" }],
};

// 计算属性
const isFormValid = computed(() => {
  const hasUsername = loginForm.username.trim().length > 0;
  const hasPassword = loginForm.password.trim().length >= 6;
  const hasCaptcha =
    !showCaptcha.value || loginForm.captcha.trim().length === 4;

  return hasUsername && hasPassword && hasCaptcha && !loading.value;
});

// 方法
const clearErrors = () => {
  errorMessage.value = "";
  if (loginFormRef.value) {
    loginFormRef.value.clearValidate();
  }
};

const clearFieldError = (field) => {
  if (loginFormRef.value) {
    loginFormRef.value.clearValidate(field);
  }
  if (errorMessage.value) {
    errorMessage.value = "";
  }
};

const validateUsername = () => {
  if (loginFormRef.value) {
    loginFormRef.value.validateFields(["username"]);
  }
};

// 获取验证码
const getCaptchaImage = async () => {
  try {
    captchaLoading.value = true;
    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 500));
    captchaImage.value =
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";
    captchaToken.value = "mock-token-" + Date.now();
  } catch (error) {
    console.error("获取验证码失败:", error);
    message.error("获取验证码失败");
  } finally {
    captchaLoading.value = false;
  }
};

const refreshCaptcha = () => {
  loginForm.captcha = "";
  getCaptchaImage();
};

// 生成二维码
const generateQrCode = async () => {
  try {
    qrStatus.value = "loading";
    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1000));
    qrImage.value =
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";
    qrToken.value = "qr-token-" + Date.now();
    qrStatus.value = "active";
    qrTimeLeft.value = 120;
    startQrTimer();
    startQrPolling();
  } catch (error) {
    console.error("生成二维码失败:", error);
    qrStatus.value = "error";
  }
};

// 二维码倒计时
const startQrTimer = () => {
  if (qrTimer.value) {
    clearInterval(qrTimer.value);
  }

  qrTimer.value = setInterval(() => {
    qrTimeLeft.value--;
    if (qrTimeLeft.value <= 0) {
      qrStatus.value = "expired";
      stopQrPolling();
      clearInterval(qrTimer.value);
    }
  }, 1000);
};

// 轮询二维码状态
const startQrPolling = () => {
  if (qrCheckTimer.value) {
    clearInterval(qrCheckTimer.value);
  }

  qrCheckTimer.value = setInterval(async () => {
    try {
      // 模拟检查二维码状态
      const random = Math.random();
      if (random < 0.1) {
        // 10%概率扫码成功
        qrStatus.value = "scanned";
        setTimeout(() => {
          // 模拟确认登录
          message.success("扫码登录成功");
          router.push("/");
          stopQrPolling();
        }, 2000);
      }
    } catch (error) {
      console.error("检查二维码状态失败:", error);
    }
  }, 2000);
};

const stopQrPolling = () => {
  if (qrCheckTimer.value) {
    clearInterval(qrCheckTimer.value);
    qrCheckTimer.value = null;
  }
  if (qrTimer.value) {
    clearInterval(qrTimer.value);
    qrTimer.value = null;
  }
};

// 处理登录
const handleLogin = async () => {
  try {
    loading.value = true;
    errorMessage.value = "";

    const loginData = {
      username: loginForm.username.trim(),
      password: loginForm.password,
      loginType: /^1[3-9]\d{9}$/.test(loginForm.username) ? "phone" : "account",
      remember: loginForm.remember,
    };

    // 如果需要验证码
    if (showCaptcha.value) {
      loginData.captcha = loginForm.captcha;
      loginData.captchaToken = captchaToken.value;
    }

    await userStore.login(loginData);

    message.success("登录成功");

    // 重置登录尝试次数
    loginAttempts.value = 0;

    // 跳转到目标页面或首页
    const redirect = route.query.redirect || "/";
    router.push(redirect);
  } catch (error) {
    console.error("登录失败:", error);

    loginAttempts.value++;

    // 处理不同类型的错误
    if (error.response?.status === 401) {
      errorMessage.value = "用户名或密码错误";
    } else if (error.response?.status === 429) {
      errorMessage.value = "登录尝试过于频繁，请稍后再试";
    } else if (error.response?.data?.code === "CAPTCHA_REQUIRED") {
      showCaptcha.value = true;
      getCaptchaImage();
      errorMessage.value = "请输入验证码";
    } else if (error.response?.data?.code === "CAPTCHA_INVALID") {
      errorMessage.value = "验证码错误";
      refreshCaptcha();
    } else {
      errorMessage.value = error.message || "登录失败，请检查用户名和密码";
    }

    // 多次失败后显示验证码
    if (loginAttempts.value >= 3 && !showCaptcha.value) {
      showCaptcha.value = true;
      getCaptchaImage();
    }
  } finally {
    loading.value = false;
  }
};

const handleLoginFailed = (errorInfo) => {
  console.log("表单验证失败:", errorInfo);
  const firstError = errorInfo.errorFields[0];
  if (firstError) {
    errorMessage.value = firstError.errors[0];
  }
};

// 忘记密码
const handleForgotPassword = () => {
  forgotPasswordVisible.value = true;
  // 获取忘记密码验证码
  refreshForgotCaptcha();
};

const refreshForgotCaptcha = async () => {
  try {
    // 模拟获取验证码
    await new Promise((resolve) => setTimeout(resolve, 500));
    forgotCaptchaImage.value =
      "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==";
    forgotCaptchaToken.value = "forgot-token-" + Date.now();
  } catch (error) {
    console.error("获取验证码失败:", error);
  }
};

const handleForgotSubmit = async () => {
  try {
    forgotLoading.value = true;

    // 模拟发送重置链接
    await new Promise((resolve) => setTimeout(resolve, 1000));

    message.success("重置链接已发送，请查收");
    forgotPasswordVisible.value = false;

    // 重置表单
    forgotForm.identifier = "";
    forgotForm.captcha = "";
  } catch (error) {
    console.error("发送重置链接失败:", error);
    message.error(error.message || "发送失败，请重试");
    refreshForgotCaptcha();
  } finally {
    forgotLoading.value = false;
  }
};

// 生命周期
onMounted(() => {
  // 检查URL参数
  if (route.query.reason === "session_expired") {
    message.warning("会话已过期，请重新登录");
  }

  // 如果已登录，直接跳转
  if (userStore.isAuthenticated) {
    router.push("/");
  }
});

onUnmounted(() => {
  stopQrPolling();
});

// 监听activeTab变化
watch(activeTab, (newTab) => {
  if (newTab === "qr") {
    generateQrCode();
  } else {
    stopQrPolling();
  }
});
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶栏样式 */
.login-header {
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  height: 80px;
  display: flex;
  align-items: center;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  background: #e60012;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.logo-image {
  width: 200px;
  height: 50px;
  display: block;
  object-fit: contain;
}

.welcome-text {
  color: #666;
  font-size: 14px;
}

.logo-welcome {
  color: #666;
  font-size: 22px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  height: 80px;
  width: 175px;
}

/* 主体区域样式 */
.login-main {
  flex: 1;
  position: relative;
  overflow: hidden;
}

.bg-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.bg-track {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  display: flex;
  transition: transform 0.6s ease-in-out;
}

.bg-slide {
  position: relative;
  height: 100%;
  background-size: cover;
  background-position: center;
  pointer-events: none;
}

.slider-dots {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 24px;
  display: flex;
  justify-content: center;
  gap: 8px;
  z-index: 3;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.6);
  cursor: pointer;
}

.dot.active {
  background: #ffffff;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 50px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: calc(100vh - 60px - 120px);
  position: relative;
  z-index: 1;
}

/* 左侧宣传区样式 */
.promo-section {
  flex: 1;
  max-width: 600px;
  color: white;
}

.promo-content {
  padding-right: 40px;
}

.main-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 16px;
  line-height: 1.3;
}

.sub-title {
  font-size: 20px;
  margin-bottom: 32px;
}

.highlight {
  color: #ffcc00;
}

.features-list {
  margin-bottom: 40px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 16px;
}

.check-icon {
  color: #4caf50;
}

.qr-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.qr-code {
  width: 80px;
  height: 80px;
}

.qr-placeholder {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 4px;
  padding: 8px;
}

.qr-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 2px;
  height: 100%;
}

.qr-dot {
  background: #333;
  border-radius: 1px;
}

.qr-text {
  font-size: 14px;
  line-height: 1.5;
}

/* 右侧登录框样式 */
.login-section {
  width: 360px;
  flex-shrink: 0;
}

.login-card {
  background: white;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.login-tabs {
  display: flex;
  border-bottom: 1px solid #e8e8e8;
}

.tab-item {
  flex: 1;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-item.active {
  color: #ff6600;
  border-bottom-color: #ff6600;
}

.tab-item:hover {
  background: #f5f5f5;
}

.login-form-container {
  padding: 24px;
}

.login-form .ant-form-item {
  margin-bottom: 16px;
}

/* 验证码样式 */
.captcha-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.captcha-container .ant-input {
  flex: 1;
}

.captcha-image {
  width: 100px;
  height: 40px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
  transition: border-color 0.3s;
}

.captcha-image:hover {
  border-color: #40a9ff;
}

.captcha-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.captcha-placeholder {
  font-size: 12px;
  color: #999;
  text-align: center;
  padding: 0 8px;
}

.captcha-tip {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* 错误提示样式 */
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #fff2f0;
  border: 1px solid #ffccc7;
  border-radius: 6px;
  color: #ff4d4f;
  font-size: 14px;
  margin-bottom: 16px;
}

.error-message .anticon {
  color: #ff4d4f;
}

.login-input {
  border-radius: 4px;
}

.login-button {
  background: #ff6600;
  border-color: #ff6600;
  border-radius: 4px;
  font-size: 16px;
  height: 44px;
}

.login-button:hover {
  background: #e55a00;
  border-color: #e55a00;
}

.login-button:disabled {
  background: #f5f5f5 !important;
  border-color: #d9d9d9 !important;
  color: #bfbfbf !important;
}

.login-links {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

.register-link {
  color: #1890ff;
}

.forgot-link {
  color: #999;
}

/* 二维码登录样式 */
.qr-login-container {
  padding: 24px;
  text-align: center;
}

.qr-login {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.qr-status {
  width: 200px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  background: #fafafa;
  transition: all 0.3s ease;
}

.qr-status.loading {
  background: #f0f0f0;
}

.qr-status.active {
  background: #fff;
  border-color: #52c41a;
}

.qr-status.scanned {
  background: #f6ffed;
  border-color: #52c41a;
}

.qr-status.expired {
  background: #fff7e6;
  border-color: #faad14;
}

.qr-status.error {
  background: #fff2f0;
  border-color: #ff4d4f;
}

.qr-code-large {
  width: 160px;
  height: 160px;
  margin: 0 auto 16px;
}

.qr-placeholder-large {
  width: 100%;
  height: 100%;
  background: #f5f5f5;
  border-radius: 4px;
  padding: 16px;
}

.qr-grid-large {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 2px;
  height: 100%;
}

.qr-instruction {
  color: #666;
  font-size: 14px;
}

.qr-timer {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

.service-time {
  padding: 16px 24px;
  background: #f9f9f9;
  border-top: 1px solid #e8e8e8;
}

.service-time p {
  margin: 0;
  font-size: 12px;
  color: #666;
  line-height: 1.4;
}

/* 页脚样式 */
.login-footer {
  background: #f5f5f5;
  padding: 30px 0;
  border-top: 1px solid #e8e8e8;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-columns {
  display: grid;
  grid-template-columns: 420px 140px 140px 140px 140px 220px;
  gap: 0;
  align-items: start;
}

.footer-columns .partner-links {
  margin-bottom: 0;
}

.partner-grid {
  display: grid;
  grid-template-columns: repeat(2, 200px);
  gap: 16px;
  justify-items: start;
  align-items: center;
}

.partner-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  padding: 10px 12px;
  height: 72px;
  box-sizing: border-box;
}

.partner-logo {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  background: #eef2f5;
  border: 1px solid #e8e8e8;
}

.partner-image {
  width: 200px;
  height: 34px;
  object-fit: contain;
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  padding: 0;
  box-sizing: border-box;
}

.qr-block h4 {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}

.qr-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.qr-code-small {
  width: 120px;
  height: 120px;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  background: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-img {
  width: 80px;
  height: 80px;
  object-fit: contain;
  display: block;
}

.qr-placeholder-small {
  width: 100%;
  height: 100%;
  padding: 10px;
}

.qr-grid-small {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 2px;
  height: 100%;
}

.account-icons {
  display: flex;
  gap: 12px;
  align-items: center;
}

.account-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #ddd;
  border: 1px solid #e8e8e8;
}

.icon-blue {
  background: #4a90e2;
}

.icon-red {
  background: #e74c3c;
}

.app-download h4 {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
}

.app-download {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.download-card {
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  background: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

.download-image {
  width: 80px;
  height: 80px;
  object-fit: contain;
  display: block;
}

.app-note {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  padding: 4px;
  margin-top: 8px;
  align-self: center;
}

.app-card {
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 4px;
  padding: 12px;
  color: #666;
  font-size: 12px;
  line-height: 1.6;
}

.partner-links {
  margin-bottom: 20px;
}

.partner-links h4 {
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
}

.partner-logos {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.partner-item {
  font-size: 12px;
  color: #666;
  padding: 4px 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e8e8e8;
}

.official-qr {
  text-align: center;
}

.qr-group {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.qr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.qr-mini {
  width: 60px;
  height: 60px;
  background: #ddd;
  border-radius: 4px;
}

.qr-item span {
  font-size: 12px;
  color: #666;
}

/* 动画效果 */
.error-message {
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 表单聚焦状态 */
.ant-input:focus,
.ant-input-password:focus {
  border-color: #ff6600;
  box-shadow: 0 0 0 2px rgba(255, 102, 0, 0.2);
}

/* 按钮悬停效果 */
.login-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
}

.login-button:active:not(:disabled) {
  transform: translateY(0);
}

/* 响应式设计 */
/* 平板设备 (768px - 1024px) */
@media (max-width: 1024px) and (min-width: 769px) {
  .main-content {
    gap: 40px;
    max-width: 900px;
  }

  .promo-content {
    padding-right: 30px;
  }

  .login-section {
    width: 340px;
  }

  .features-list {
    margin-bottom: 30px;
  }

  .qr-section {
    padding: 16px;
  }
}

/* 平板设备 (768px及以下) */
@media (max-width: 768px) {
  .header-content {
    padding: 0 16px;
  }

  .main-content {
    flex-direction: column;
    gap: 24px;
    padding: 30px 16px;
  }

  .promo-section {
    max-width: none;
    text-align: center;
    order: 2; /* 移动端将推广区域放到登录框下方 */
  }

  .promo-content {
    padding-right: 0;
  }

  .login-section {
    width: 100%;
    max-width: 400px;
    order: 1; /* 登录框优先显示 */
  }

  .qr-section {
    justify-content: center;
  }

  .partner-logos {
    justify-content: center;
  }

  .qr-group {
    gap: 20px;
  }

  .captcha-container {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }

  .captcha-image {
    width: 100%;
    height: 50px;
  }

  .qr-status {
    width: 180px;
    height: 180px;
  }

  .tab-item {
    font-size: 15px;
    padding: 12px 16px;
  }

  .main-title {
    font-size: 26px;
  }

  .sub-title {
    font-size: 19px;
  }
}

/* 手机设备 (480px及以下) */
@media (max-width: 480px) {
  .header-content {
    padding: 0 12px;
  }

  .logo-section {
    flex-direction: column;
    gap: 6px;
    align-items: flex-start;
  }

  .welcome-text {
    font-size: 13px;
  }

  .main-content {
    padding: 20px 12px;
  }

  .main-title {
    font-size: 22px;
  }

  .sub-title {
    font-size: 17px;
  }

  .login-card {
    margin: 0 12px;
  }

  .login-form-container {
    padding: 20px 16px;
  }

  .qr-login-container {
    padding: 20px 16px;
  }

  .qr-group {
    flex-direction: column;
    gap: 15px;
  }

  .qr-code-large {
    width: 140px;
    height: 140px;
  }

  .feature-item {
    font-size: 15px;
  }

  .login-button {
    height: 42px;
    font-size: 15px;
  }

  .tab-item {
    font-size: 14px;
    padding: 10px 12px;
  }
}

/* 超小屏幕设备 (360px及以下) */
@media (max-width: 360px) {
  .header-content {
    padding: 0 8px;
  }

  .welcome-text {
    display: none; /* 超小屏幕隐藏欢迎文字 */
  }

  .main-content {
    padding: 16px 8px;
  }

  .login-card {
    margin: 0 8px;
  }

  .login-form-container {
    padding: 16px 12px;
  }

  .qr-login-container {
    padding: 16px 12px;
  }

  .main-title {
    font-size: 20px;
  }

  .sub-title {
    font-size: 16px;
  }

  .tab-item {
    font-size: 13px;
    padding: 8px 10px;
  }

  .login-button {
    height: 40px;
    font-size: 14px;
  }

  .qr-code-large {
    width: 120px;
    height: 120px;
  }

  .footer-content {
    padding: 0 8px;
  }

  .qr-mini {
    width: 50px;
    height: 50px;
  }

  .qr-item span {
    font-size: 11px;
  }
}

@media (max-width: 1024px) and (min-width: 769px) {
  .footer-columns {
    grid-template-columns: repeat(3, 1fr);
  }
  .partner-links {
    grid-column: span 3;
  }
}

@media (max-width: 768px) {
  .footer-columns {
    grid-template-columns: 1fr;
    gap: 24px;
  }
  .qr-block {
    text-align: center;
  }

  .partner-grid {
    grid-template-columns: 1fr;
    justify-items: center;
  }

  .partner-image {
    width: 200px;
  }
}

@media (max-width: 480px) {
  .qr-code-small {
    width: 100px;
    height: 100px;
  }
}

@media (max-width: 360px) {
  .qr-code-small {
    width: 90px;
    height: 90px;
  }
}
</style>
