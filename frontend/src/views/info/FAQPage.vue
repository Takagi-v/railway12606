<template>
  <div class="info-page">
    <div class="container">
      <h1>常见问题</h1>
      <div class="info-content">
        <div class="faq-list">
          <div class="faq-item" v-for="item in faqs" :key="item.id">
            <div class="faq-question" @click="toggleFAQ(item.id)">
              <span>{{ item.question }}</span>
              <span class="toggle-icon">{{ item.expanded ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="item.expanded">
              {{ item.answer }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const faqs = ref([
  {
    id: 1,
    question: '如何注册12306账号？',
    answer: '您可以通过12306官网或手机APP进行注册，需要提供真实姓名、身份证号码、手机号码等信息。',
    expanded: false
  },
  {
    id: 2,
    question: '忘记密码怎么办？',
    answer: '可以通过注册时绑定的手机号码或邮箱找回密码，也可以到车站窗口进行密码重置。',
    expanded: false
  },
  {
    id: 3,
    question: '如何改签车票？',
    answer: '在车票发车前，可以通过12306网站、手机APP或车站窗口办理改签手续。',
    expanded: false
  }
])

const toggleFAQ = id => {
  const faq = faqs.value.find(item => item.id === id)
  if (faq) {
    faq.expanded = !faq.expanded
  }
}
</script>

<style scoped>
.info-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 50px 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.faq-item {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
}

.faq-question {
  padding: 20px;
  background: #f8f9fa;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: #2c3e50;
  transition: background 0.3s;
}

.faq-question:hover {
  background: #e9ecef;
}

.toggle-icon {
  font-size: 20px;
  font-weight: bold;
}

.faq-answer {
  padding: 20px;
  color: #666;
  line-height: 1.6;
  border-top: 1px solid #e0e0e0;
}
</style>
