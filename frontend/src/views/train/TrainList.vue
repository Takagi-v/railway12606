<template>
  <a-layout class="train-list-layout">
    <app-header />
    <a-layout-content class="train-list-content">
      <div class="content-wrapper">
        <a-card class="search-info" :bordered="false">
          <div class="search-summary">
            <span class="route">{{ query.departure_city }} → {{ query.arrival_city }}</span>
            <span class="date">{{ query.travel_date }}</span>
            <a-button type="link" @click="router.push('/')">修改查询</a-button>
          </div>
        </a-card>

        <a-card class="train-list-card">
          <a-spin :spinning="loading">
            <template v-if="trains.length > 0">
              <a-table
                :data-source="trains"
                :columns="columns"
                :pagination="false"
                row-key="train_id"
              />
            </template>
            <template v-else>
              <a-empty description="暂无车次数据，请稍后再试">
                <a-button type="primary" @click="router.push('/')">返回首页</a-button>
              </a-empty>
            </template>
          </a-spin>
        </a-card>
      </div>
    </a-layout-content>
    <app-footer />
  </a-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { searchTrains } from '@/api/train'

const router = useRouter()
const route = useRoute()

const query = ref(route.query)
const trains = ref([])
const loading = ref(false)

const columns = [
  { title: '车次', dataIndex: 'train_number', key: 'train_number' },
  { title: '类型', dataIndex: 'train_type', key: 'train_type' },
  { title: '出发站', dataIndex: 'departure_station', key: 'departure_station' },
  { title: '到达站', dataIndex: 'arrival_station', key: 'arrival_station' },
  { title: '出发时间', dataIndex: 'departure_time', key: 'departure_time' },
  { title: '到达时间', dataIndex: 'arrival_time', key: 'arrival_time' },
  { title: '历时', dataIndex: 'duration', key: 'duration' },
  {
    title: '一等座',
    key: 'first_class',
    customRender: ({ record }) =>
      `${record.first_class.available} 张 / ¥${record.first_class.price}`
  },
  {
    title: '二等座',
    key: 'second_class',
    customRender: ({ record }) =>
      `${record.second_class.available} 张 / ¥${record.second_class.price}`
  },
  {
    title: '软卧',
    key: 'soft_sleeper',
    customRender: ({ record }) =>
      `${record.soft_sleeper.available} 张 / ¥${record.soft_sleeper.price}`
  },
  {
    title: '硬卧',
    key: 'hard_sleeper',
    customRender: ({ record }) =>
      `${record.hard_sleeper.available} 张 / ¥${record.hard_sleeper.price}`
  }
]

onMounted(async () => {
  loading.value = true
  try {
    const res = await searchTrains({
      departure_city: query.value.departure_city,
      arrival_city: query.value.arrival_city,
      travel_date: query.value.travel_date
    })
    trains.value = res?.data || []
  } catch (e) {
    console.error('加载车次失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.train-list-layout {
  min-height: 100vh;
}

.train-list-content {
  background: #f0f2f5;
  min-height: calc(100vh - 64px - 70px);
  padding: 20px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.search-info {
  margin-bottom: 20px;
}

.search-summary {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 16px;
}

.route {
  font-weight: bold;
  font-size: 18px;
}

.train-list-card {
  min-height: 400px;
}

.placeholder-text {
  text-align: center;
  padding: 100px 20px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 16px;
  line-height: 2;
}
</style>
