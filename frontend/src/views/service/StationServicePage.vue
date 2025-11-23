<template>
  <div class="service-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="header">
        <h1>站车风采</h1>
        <p class="subtitle">展示铁路系统优质服务，传递温暖出行体验</p>
      </div>

      <!-- 筛选器 -->
      <div class="filter-section">
        <div class="filter-tabs">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            :class="['tab-btn', { active: activeTab === tab.key }]"
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="filter-controls">
          <select v-model="selectedRegion" class="filter-select">
            <option value="">全部地区</option>
            <option v-for="region in regions" :key="region" :value="region">
              {{ region }}
            </option>
          </select>

          <select v-model="selectedType" class="filter-select">
            <option value="">全部类型</option>
            <option v-for="type in serviceTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>
        </div>
      </div>

      <!-- 内容展示区 -->
      <div class="content-section">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>正在加载精彩内容...</p>
        </div>

        <!-- 内容网格 -->
        <div v-else class="content-grid">
          <div
            v-for="item in filteredItems"
            :key="item.id"
            class="content-card"
            @click="openDetail(item)"
          >
            <div class="card-image">
              <img :src="item.image" :alt="item.title" />
              <div class="card-overlay">
                <span class="card-type">{{ item.type }}</span>
                <span class="card-region">{{ item.region }}</span>
              </div>
            </div>

            <div class="card-content">
              <h3 class="card-title">{{ item.title }}</h3>
              <p class="card-description">{{ item.description }}</p>

              <div class="card-meta">
                <div class="meta-item">
                  <span class="icon">📍</span>
                  <span>{{ item.location }}</span>
                </div>
                <div class="meta-item">
                  <span class="icon">📅</span>
                  <span>{{ formatDate(item.date) }}</span>
                </div>
              </div>

              <div class="card-stats">
                <div class="stat-item">
                  <span class="icon">👍</span>
                  <span>{{ item.likes }}</span>
                </div>
                <div class="stat-item">
                  <span class="icon">👁️</span>
                  <span>{{ item.views }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && filteredItems.length === 0" class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>暂无相关内容</h3>
          <p>请尝试调整筛选条件或稍后再试</p>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="!loading && filteredItems.length > 0" class="pagination">
        <button :disabled="currentPage === 1" @click="currentPage--" class="page-btn">
          上一页
        </button>

        <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>

        <button :disabled="currentPage === totalPages" @click="currentPage++" class="page-btn">
          下一页
        </button>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div v-if="showDetail" class="detail-modal" @click="closeDetail">
      <div class="detail-content" @click.stop>
        <button class="close-btn" @click="closeDetail">×</button>

        <div class="detail-header">
          <img :src="selectedItem.image" :alt="selectedItem.title" />
          <div class="detail-info">
            <h2>{{ selectedItem.title }}</h2>
            <div class="detail-meta">
              <span class="badge">{{ selectedItem.type }}</span>
              <span class="location">📍 {{ selectedItem.location }}</span>
              <span class="date">📅 {{ formatDate(selectedItem.date) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-body">
          <p>{{ selectedItem.fullDescription }}</p>

          <div class="service-highlights">
            <h3>服务亮点</h3>
            <ul>
              <li v-for="highlight in selectedItem.highlights" :key="highlight">
                {{ highlight }}
              </li>
            </ul>
          </div>

          <div class="contact-info">
            <h3>联系方式</h3>
            <p>服务热线：{{ selectedItem.contact }}</p>
            <p>服务时间：{{ selectedItem.serviceTime }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 响应式数据
const loading = ref(true)
const activeTab = ref('all')
const selectedRegion = ref('')
const selectedType = ref('')
const currentPage = ref(1)
const showDetail = ref(false)
const selectedItem = ref({})

// 标签页配置
const tabs = [
  { key: 'all', label: '全部' },
  { key: 'station', label: '车站服务' },
  { key: 'train', label: '列车服务' },
  { key: 'special', label: '特色服务' }
]

// 筛选选项
const regions = ['华北地区', '华东地区', '华南地区', '华中地区', '西南地区', '西北地区', '东北地区']
const serviceTypes = ['便民服务', '无障碍服务', '特殊旅客服务', '应急服务', '文化服务']

// 模拟数据
const serviceItems = ref([
  {
    id: 1,
    title: '北京南站"爱心服务"',
    description: '为特殊旅客提供全程无障碍服务，温暖每一次出行',
    fullDescription:
      '北京南站"爱心服务"团队致力于为老、幼、病、残、孕等特殊旅客提供全方位的出行服务。从进站到上车，从候车到送站，每一个环节都体现着铁路人的温暖关怀。',
    image: 'https://via.placeholder.com/400x250/4CAF50/white?text=爱心服务',
    type: '特殊旅客服务',
    region: '华北地区',
    location: '北京南站',
    date: '2024-01-15',
    likes: 1256,
    views: 8934,
    category: 'station',
    highlights: [
      '24小时爱心服务台',
      '专业手语服务员',
      '无障碍通道引导',
      '轮椅租借服务',
      '重点旅客预约服务'
    ],
    contact: '010-12306',
    serviceTime: '全天24小时'
  },
  {
    id: 2,
    title: 'G1次列车"微笑服务"',
    description: '用真诚的微笑传递温暖，让旅途更加美好',
    fullDescription:
      'G1次列车乘务组以"微笑服务"为理念，用真诚的笑容和贴心的服务，为每一位旅客营造温馨舒适的旅行环境。',
    image: 'https://via.placeholder.com/400x250/2196F3/white?text=微笑服务',
    type: '便民服务',
    region: '华东地区',
    location: 'G1次列车',
    date: '2024-01-20',
    likes: 892,
    views: 5647,
    category: 'train',
    highlights: [
      '标准化微笑服务',
      '多语言服务能力',
      '个性化需求满足',
      '应急处理专业',
      '文明礼仪规范'
    ],
    contact: '12306',
    serviceTime: '运行期间'
  },
  {
    id: 3,
    title: '上海虹桥站"智慧服务"',
    description: '运用科技力量，提升服务效率和旅客体验',
    fullDescription:
      '上海虹桥站积极运用人工智能、大数据等先进技术，打造智慧化服务体系，为旅客提供更加便捷高效的出行服务。',
    image: 'https://via.placeholder.com/400x250/FF9800/white?text=智慧服务',
    type: '便民服务',
    region: '华东地区',
    location: '上海虹桥站',
    date: '2024-01-25',
    likes: 1543,
    views: 12456,
    category: 'station',
    highlights: ['AI智能问询系统', '人脸识别进站', '自助服务设备', '实时信息推送', '智能导航服务'],
    contact: '021-12306',
    serviceTime: '全天24小时'
  },
  {
    id: 4,
    title: '广州南站"文化服务"',
    description: '传承岭南文化，展示地方特色，丰富旅途体验',
    fullDescription:
      '广州南站将岭南文化融入服务中，通过文化展示、特色表演等形式，让旅客在候车过程中感受浓郁的地方文化氛围。',
    image: 'https://via.placeholder.com/400x250/E91E63/white?text=文化服务',
    type: '文化服务',
    region: '华南地区',
    location: '广州南站',
    date: '2024-02-01',
    likes: 756,
    views: 4321,
    category: 'special',
    highlights: ['岭南文化展示', '传统艺术表演', '地方特产推介', '文化讲解服务', '互动体验活动'],
    contact: '020-12306',
    serviceTime: '06:00-24:00'
  },
  {
    id: 5,
    title: 'D2566次"母婴关爱"服务',
    description: '专为母婴旅客打造的贴心服务，让亲子出行更安心',
    fullDescription:
      'D2566次列车专门设置母婴关爱服务，为带婴幼儿出行的旅客提供专业、贴心的服务保障。',
    image: 'https://via.placeholder.com/400x250/9C27B0/white?text=母婴关爱',
    type: '特殊旅客服务',
    region: '华中地区',
    location: 'D2566次列车',
    date: '2024-02-05',
    likes: 634,
    views: 3789,
    category: 'train',
    highlights: ['母婴专用候车区', '婴儿用品提供', '哺乳室服务', '儿童餐食定制', '安全座椅配备'],
    contact: '12306',
    serviceTime: '运行期间'
  },
  {
    id: 6,
    title: '成都东站"应急救援"',
    description: '专业应急救援团队，保障旅客出行安全',
    fullDescription:
      '成都东站建立了专业的应急救援体系，配备专业救援设备和医疗人员，为旅客提供及时有效的应急救援服务。',
    image: 'https://via.placeholder.com/400x250/F44336/white?text=应急救援',
    type: '应急服务',
    region: '西南地区',
    location: '成都东站',
    date: '2024-02-10',
    likes: 423,
    views: 2156,
    category: 'station',
    highlights: ['24小时医疗站', '专业救援设备', '应急预案完善', '快速响应机制', '医护人员常驻'],
    contact: '028-12306',
    serviceTime: '全天24小时'
  }
])

// 计算属性
const filteredItems = computed(() => {
  let items = serviceItems.value

  // 按标签页筛选
  if (activeTab.value !== 'all') {
    items = items.filter(item => item.category === activeTab.value)
  }

  // 按地区筛选
  if (selectedRegion.value) {
    items = items.filter(item => item.region === selectedRegion.value)
  }

  // 按类型筛选
  if (selectedType.value) {
    items = items.filter(item => item.type === selectedType.value)
  }

  return items
})

const totalPages = computed(() => {
  return Math.ceil(filteredItems.value.length / 6)
})

// 方法
const formatDate = dateStr => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const openDetail = item => {
  selectedItem.value = item
  showDetail.value = true
  document.body.style.overflow = 'hidden'
}

const closeDetail = () => {
  showDetail.value = false
  document.body.style.overflow = 'auto'
}

// 生命周期
onMounted(() => {
  // 模拟加载
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>

<style scoped>
.service-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px;
  text-align: center;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.subtitle {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.6;
}

/* 筛选器样式 */
.filter-section {
  padding: 30px 40px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-tabs {
  display: flex;
  gap: 10px;
}

.tab-btn {
  padding: 10px 20px;
  border: 2px solid #e1e8ed;
  background: white;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.tab-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.filter-controls {
  display: flex;
  gap: 15px;
}

.filter-select {
  padding: 10px 15px;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
}

/* 内容区域样式 */
.content-section {
  padding: 40px;
  min-height: 400px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #666;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

.content-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.content-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.content-card:hover .card-image img {
  transform: scale(1.05);
}

.card-overlay {
  position: absolute;
  top: 15px;
  left: 15px;
  display: flex;
  gap: 10px;
}

.card-type,
.card-region {
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.card-content {
  padding: 20px;
}

.card-title {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.card-description {
  margin: 0 0 15px 0;
  color: #666;
  line-height: 1.5;
  font-size: 0.9rem;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: #666;
}

.meta-item .icon {
  font-size: 1rem;
}

.card-stats {
  display: flex;
  justify-content: space-between;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.85rem;
  color: #666;
}

/* 空状态样式 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 30px 40px;
  border-top: 1px solid #eee;
}

.page-btn {
  padding: 10px 20px;
  border: 2px solid #667eea;
  background: white;
  color: #667eea;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.page-btn:hover:not(:disabled) {
  background: #667eea;
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-weight: 500;
}

/* 详情弹窗样式 */
.detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.detail-content {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  z-index: 1001;
  transition: background 0.3s ease;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.2);
}

.detail-header {
  position: relative;
}

.detail-header img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.detail-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
  padding: 40px 30px 30px;
}

.detail-info h2 {
  margin: 0 0 15px 0;
  font-size: 2rem;
  font-weight: 700;
}

.detail-meta {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
}

.location,
.date {
  font-size: 0.9rem;
  opacity: 0.9;
}

.detail-body {
  padding: 30px;
}

.detail-body p {
  line-height: 1.8;
  color: #555;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

.service-highlights,
.contact-info {
  margin-bottom: 30px;
}

.service-highlights h3,
.contact-info h3 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.service-highlights ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.service-highlights li {
  padding: 8px 0;
  color: #555;
  position: relative;
  padding-left: 20px;
}

.service-highlights li::before {
  content: '✓';
  color: #667eea;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.contact-info p {
  margin: 8px 0;
  color: #555;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-tabs {
    justify-content: center;
  }

  .filter-controls {
    justify-content: center;
  }

  .content-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .service-page {
    padding: 10px;
  }

  .container {
    margin: 0 10px;
    border-radius: 12px;
  }

  .header {
    padding: 30px 20px;
  }

  .header h1 {
    font-size: 2rem;
  }

  .content-section {
    padding: 20px;
  }

  .filter-section {
    padding: 20px;
  }

  .filter-tabs {
    flex-wrap: wrap;
  }

  .tab-btn {
    padding: 8px 16px;
    font-size: 0.9rem;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .pagination {
    padding: 20px;
  }

  .detail-content {
    margin: 10px;
    max-height: calc(100vh - 20px);
  }

  .detail-info h2 {
    font-size: 1.5rem;
  }

  .detail-meta {
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .filter-controls {
    flex-direction: column;
    width: 100%;
  }

  .filter-select {
    width: 100%;
  }

  .card-content {
    padding: 15px;
  }

  .detail-body {
    padding: 20px;
  }
}

/* 无障碍支持 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .tab-btn,
  .filter-select,
  .page-btn {
    border-width: 2px;
  }

  .content-card {
    border: 2px solid #ccc;
  }
}
</style>
