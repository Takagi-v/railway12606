<template>
  <div
    class="city-search"
    v-show="visible"
    :style="{ top: top + 'px', left: left + 'px' }"
    @mousedown.prevent
  >
    <div class="form-cities">
      <div class="top-cities">
        按"<span class="txt-primary">{{ searchQuery }}</span>"检索：
      </div>
      <div class="panel-cities">
        <div
          v-for="(city, index) in pagedCities"
          :key="city.code"
          :class="['cityline', { citylineover: index === selectedIndex }]"
          @click="selectCity(city)"
          @mouseenter="selectedIndex = index"
        >
          <span class="ralign name">{{ city.name }}</span>
          <span class="ralign code">{{ city.code }}</span>
        </div>
        <div v-if="filteredCities.length === 0" class="no-result">
          无匹配城市
        </div>
      </div>
      <div class="flip-cities" v-if="totalPages > 1">
        <div class="citypage">
          <a href="#" class="pagetxt" @click.prevent="prevPage" :class="{ disabled: currentPage === 1 }">&lt;&lt;</a>
          <span class="page-info">{{ currentPage }}/{{ totalPages }}</span>
          <a href="#" class="pagetxt" @click.prevent="nextPage" :class="{ disabled: currentPage === totalPages }">&gt;&gt;</a>
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
  left: { type: Number, default: 0 },
  searchQuery: { type: String, default: '' }
})

const emit = defineEmits(['select', 'close'])

const currentPage = ref(1)
const pageSize = 6
const selectedIndex = ref(-1)

// Flatten all cities for search
const allCities = computed(() => {
  const cities = [...hotCities]
  // Use a Set to avoid duplicates if hotCities are also in cityData
  const seen = new Set(cities.map(c => c.code))
  
  for (const group in cityData) {
    for (const letter in cityData[group]) {
      cityData[group][letter].forEach(city => {
        if (!seen.has(city.code)) {
          cities.push(city)
          seen.add(city.code)
        }
      })
    }
  }
  return cities
})

const filteredCities = computed(() => {
  if (!props.searchQuery) return []
  const query = props.searchQuery.toLowerCase()
  return allCities.value.filter(city => 
    city.name.includes(query) || 
    city.code.toLowerCase().includes(query)
  )
})

const totalPages = computed(() => Math.ceil(filteredCities.value.length / pageSize))

const pagedCities = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredCities.value.slice(start, start + pageSize)
})

const selectCity = (city) => {
  emit('select', city.name)
  emit('close')
}

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++
}

watch(() => props.searchQuery, () => {
  currentPage.value = 1
  selectedIndex.value = -1
})
</script>

<style scoped>
.city-search {
  position: absolute;
  z-index: 2001; /* Higher than selector */
  font-size: 12px;
  font-family: 'Microsoft YaHei', sans-serif;
}

.form-cities {
  width: 220px;
  border: 1px solid #298cce; /* Blue border */
  background: #fff;
  box-shadow: 2px 2px 3px rgba(0,0,0,0.3);
}

.top-cities {
  padding: 5px;
  background-color: #fff; /* White background */
  border-bottom: 1px solid #ccc;
  color: #333;
}

.txt-primary {
  color: #FF8200; /* Orange color for highlight */
  font-weight: bold;
}

.panel-cities {
  max-height: 200px;
  overflow-y: auto;
}

.cityline {
  padding: 5px;
  cursor: pointer;
  overflow: hidden;
  line-height: 20px;
  color: #333;
}

.cityline:hover, .citylineover {
  background-color: #c8e3fc; /* Light blue background */
  color: #0055AA; /* Blue text on hover */
}

.ralign.name {
  float: left;
}

.ralign.code {
  float: right;
  font-family: monospace;
  color: inherit;
}

.no-result {
  padding: 10px;
  text-align: center;
  color: #333;
}

.flip-cities {
  padding: 5px;
  text-align: center;
  background-color: #fff; /* White background */
  border-top: 1px solid #ccc;
}

.citypage {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagetxt {
  text-decoration: none;
  color: #0077FF;
  padding: 0 5px;
  cursor: pointer;
}

.pagetxt.disabled {
  color: #ccc;
  cursor: default;
}

.page-info {
  color: #333;
}
</style>
