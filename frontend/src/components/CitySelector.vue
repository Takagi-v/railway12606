<template>
  <div
    class="city-selector"
    v-show="visible"
    :style="{ top: top + 'px', left: left + 'px' }"
    @mousedown.prevent
  >
    <!-- Left Sidebar -->
    <div class="city-selector-sidebar">
      <div class="sidebar-item active">国内站点</div>
      <div class="sidebar-item">国际站点</div>
    </div>

    <!-- Right Content Area -->
    <div class="city-selector-main">
      <!-- Header -->
      <div class="city-selector-header">
        拼音支持首字母输入
      </div>

      <!-- Tabs -->
      <div class="city-selector-tabs">
        <div
          v-for="tab in tabs"
          :key="tab.key"
          class="city-selector-tab"
          :class="{ active: currentTab === tab.key }"
          @click="currentTab = tab.key"
        >
          {{ tab.label }}
        </div>
      </div>

      <!-- City List Content -->
      <div class="city-selector-content">
        <div v-if="currentTab === 'hot'" class="city-list hot-list">
          <div
            v-for="city in hotCities"
            :key="city.code"
            class="city-item"
            @click="selectCity(city)"
          >
            {{ city.name }}
          </div>
        </div>
        <div v-else class="city-list-group-container">
          <div v-for="(cities, letter) in currentCitiesGroup" :key="letter" class="city-group-row">
            <div class="city-group-letter">{{ letter }}</div>
            <div class="city-group-list">
              <div
                v-for="city in cities"
                :key="city.code"
                class="city-item"
                @click="selectCity(city)"
              >
                {{ city.name }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer / Pagination -->
      <div class="city-selector-footer" v-if="currentTab !== 'hot' && totalPages > 1">
        <div class="pagination-controls">
          <span
            class="page-btn"
            :class="{ disabled: currentPage === 1 }"
            @click="currentPage > 1 && (currentPage--)"
          >
            &laquo; 上一页
          </span>
          <span class="page-info"></span>
          <span
            class="page-btn"
            :class="{ disabled: currentPage === totalPages }"
            @click="currentPage < totalPages && (currentPage++)"
          >
            下一页 &raquo;
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { hotCities, cityData } from '@/utils/cityData'

const props = defineProps({
  visible: Boolean,
  top: { type: Number, default: 0 },
  left: { type: Number, default: 0 }
})

const emit = defineEmits(['select', 'close'])

const tabs = [
  { key: 'hot', label: '热门' },
  { key: 'ABCDE', label: 'ABCDE' },
  { key: 'FGHIJ', label: 'FGHIJ' },
  { key: 'KLMNO', label: 'KLMNO' },
  { key: 'PQRST', label: 'PQRST' },
  { key: 'UVWXYZ', label: 'UVWXYZ' }
]

const currentTab = ref('hot')
const currentPage = ref(1)
const itemsPerLetterPage = 12 // 2 rows of 6

const totalPages = computed(() => {
  if (currentTab.value === 'hot') return 1
  const groups = cityData[currentTab.value] || {}
  let maxLen = 0
  for (const letter in groups) {
    if (groups[letter].length > maxLen) {
      maxLen = groups[letter].length
    }
  }
  return Math.ceil(maxLen / itemsPerLetterPage)
})

const currentCitiesGroup = computed(() => {
  if (currentTab.value === 'hot') return {}
  
  const groups = cityData[currentTab.value] || {}
  const pagedGroups = {}
  
  for (const letter in groups) {
    const start = (currentPage.value - 1) * itemsPerLetterPage
    const end = start + itemsPerLetterPage
    pagedGroups[letter] = groups[letter].slice(start, end)
  }
  
  return pagedGroups
})

const selectCity = (city) => {
  emit('select', city.name)
  emit('close')
}

watch(currentTab, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.city-selector {
  position: absolute;
  width: 580px;
  background: #fff;
  border: 1px solid #ddd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 2000;
  font-size: 12px;
  display: flex;
  font-family: 'Microsoft YaHei', sans-serif;
}

/* Sidebar Styles */
.city-selector-sidebar {
  width: 90px;
  background-color: #f8f8f8;
  border-right: 1px solid #eee;
  flex-shrink: 0;
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar-item {
  width: 76px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  cursor: pointer;
  color: #333;
  margin-bottom: 5px;
  border-radius: 4px;
}

.sidebar-item:hover {
  background-color: #eee;
}

.sidebar-item.active {
  background-color: #3B99FC;
  color: #fff;
}

/* Main Content Styles */
.city-selector-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.city-selector-header {
  padding: 10px 15px;
  color: #666;
  border-bottom: 1px solid #eee;
}

/* Tabs Styles */
.city-selector-tabs {
  display: flex;
  background: #EAF4FF;
  padding: 0 10px;
}

.city-selector-tab {
  padding: 8px 15px;
  cursor: pointer;
  color: #333;
  border-bottom: 2px solid transparent; /* Reserve space for border */
  margin-bottom: -1px; /* Align with bottom */
}

.city-selector-tab.active {
  color: #3B99FC;
  border-bottom: 2px solid #3B99FC;
  font-weight: bold;
}

.city-selector-tab:hover {
  color: #3B99FC;
}

/* Content Styles */
.city-selector-content {
  padding: 10px 15px;
  min-height: 200px;
  background: #fff;
}

.city-list {
  display: flex;
  flex-wrap: wrap;
}

.city-item {
  width: 16.66%; /* 6 items per row */
  height: 24px;
  line-height: 24px;
  cursor: pointer;
  color: #333;
  padding-left: 5px;
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.city-item:hover {
  background-color: #3B99FC;
  color: #fff;
  border-radius: 2px;
}

/* Grouped List Styles */
.city-group-row {
  display: flex;
  margin-bottom: 5px;
}

.city-group-letter {
  width: 30px;
  font-weight: bold;
  color: #3B99FC;
  text-align: center;
  padding-top: 2px;
  flex-shrink: 0;
}

.city-group-list {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
}

/* Footer Styles */
.city-selector-footer {
  padding: 5px 10px;
  text-align: right;
  border-top: 1px solid #eee;
}

.pagination-controls {
  display: inline-block;
}

.page-btn {
  display: inline-block;
  padding: 2px 8px;
  margin-left: 10px;
  cursor: pointer;
  color: #333;
}

.page-btn:hover {
  color: #3B99FC;
  text-decoration: underline;
}

.page-btn.disabled {
  color: #ccc;
  cursor: not-allowed;
  text-decoration: none;
}
</style>
