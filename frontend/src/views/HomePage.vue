<template>
  <a-layout class="home-layout">
    <app-header />
    <a-layout-content class="home-content">
      <div class="search-section">
        <h1 class="title">欢迎使用中国铁路12306购票系统</h1>
        
        <a-card class="search-card">
          <a-form
            :model="searchForm"
            layout="inline"
            class="search-form"
            @finish="handleSearch"
          >
            <a-form-item label="出发地" name="departureCity" :rules="[{ required: true, message: '请选择出发地' }]">
              <a-input
                v-model:value="searchForm.departureCity"
                placeholder="请输入出发地"
                style="width: 200px"
              />
            </a-form-item>
            
            <a-form-item>
              <a-button type="link" @click="swapCities">
                <SwapOutlined />
              </a-button>
            </a-form-item>
            
            <a-form-item label="目的地" name="arrivalCity" :rules="[{ required: true, message: '请选择目的地' }]">
              <a-input
                v-model:value="searchForm.arrivalCity"
                placeholder="请输入目的地"
                style="width: 200px"
              />
            </a-form-item>
            
            <a-form-item label="出发日期" name="travelDate" :rules="[{ required: true, message: '请选择出发日期' }]">
              <a-date-picker
                v-model:value="searchForm.travelDate"
                style="width: 200px"
                :disabled-date="disabledDate"
                placeholder="选择日期"
              />
            </a-form-item>
            
            <a-form-item>
              <a-button type="primary" html-type="submit" size="large">
                <SearchOutlined /> 查询
              </a-button>
            </a-form-item>
          </a-form>
        </a-card>
        
        <div class="quick-links">
          <a-card title="快捷入口" :bordered="false">
            <a-row :gutter="16">
              <a-col :span="8">
                <a-button type="link" size="large" @click="router.push('/user/orders')" block>
                  <FileTextOutlined /> 订单查询
                </a-button>
              </a-col>
              <a-col :span="8">
                <a-button type="link" size="large" @click="router.push('/user/passengers')" block>
                  <TeamOutlined /> 乘客管理
                </a-button>
              </a-col>
              <a-col :span="8">
                <a-button type="link" size="large" @click="router.push('/user/profile')" block>
                  <UserOutlined /> 个人中心
                </a-button>
              </a-col>
            </a-row>
          </a-card>
        </div>
      </div>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { SearchOutlined, SwapOutlined, FileTextOutlined, TeamOutlined, UserOutlined } from '@ant-design/icons-vue'

const router = useRouter()

const searchForm = ref({
  departureCity: '',
  arrivalCity: '',
  travelDate: dayjs()
})

const disabledDate = (current) => {
  // 只能选择今天到未来30天
  return current && (current < dayjs().startOf('day') || current > dayjs().add(30, 'day'))
}

const swapCities = () => {
  const temp = searchForm.value.departureCity
  searchForm.value.departureCity = searchForm.value.arrivalCity
  searchForm.value.arrivalCity = temp
}

const handleSearch = () => {
  const params = {
    departure_city: searchForm.value.departureCity,
    arrival_city: searchForm.value.arrivalCity,
    travel_date: searchForm.value.travelDate.format('YYYY-MM-DD')
  }
  
  router.push({
    name: 'trains',
    query: params
  })
}
</script>

<style scoped>
.home-layout {
  min-height: 100vh;
}

.home-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: calc(100vh - 64px - 70px);
  padding: 50px 20px;
}

.search-section {
  max-width: 1000px;
  margin: 0 auto;
}

.title {
  color: white;
  text-align: center;
  font-size: 32px;
  margin-bottom: 40px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.search-card {
  margin-bottom: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.quick-links {
  margin-top: 30px;
}

.quick-links :deep(.ant-card) {
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
}
</style>

