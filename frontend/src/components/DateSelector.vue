<template>
  <div
    class="cal-wrap"
    v-show="visible"
    :style="{ top: top + 'px', left: left + 'px', zIndex: 30000, position: 'absolute', display: 'block' }"
    @mousedown.prevent
  >
    <!-- Left Calendar -->
    <div class="cal">
      <div class="cal-top">
        <a href="javascript:void(0);" class="first" @click="prevYear"></a>
        <a href="javascript:void(0);" class="prev" @click="prevMonth"></a>
        <div class="month">
          <input type="text" :value="leftMonthLabel" readonly="readonly" style="cursor: pointer;">
          <!-- Month dropdown could go here -->
        </div>
        <div class="year">
          <input type="text" :value="leftYearLabel" readonly="readonly" style="cursor: pointer;">
          <!-- Year dropdown could go here -->
        </div>
      </div>
      <ul class="cal-week">
        <li><b>日</b></li>
        <li>一</li>
        <li>二</li>
        <li>三</li>
        <li>四</li>
        <li>五</li>
        <li><b>六</b></li>
      </ul>
      <div class="cal-cm" style="height: 115px;">
        <div
          v-for="(day, index) in leftDays"
          :key="'left-' + index"
          class="cell"
          :style="{ left: day.left + 'px', top: day.top + 'px', cursor: day.enabled ? 'pointer' : 'default' }"
          @click="day.enabled && selectDate(day.date)"
          :class="{ 'disabled': !day.enabled, 'selected': isSelected(day.date) }"
        >
          <div class="so" :style="{ color: getDayColor(day) }">
            {{ day.text }}
          </div>
        </div>
      </div>
    </div>

    <!-- Right Calendar -->
    <div class="cal cal-right">
      <div class="cal-top">
        <a href="javascript:void(0);" class="last" @click="nextYear"></a>
        <a href="javascript:void(0);" class="next" @click="nextMonth"></a>
        <div class="year">
          <input type="text" :value="rightYearLabel" readonly="readonly" style="cursor: pointer;">
        </div>
        <div class="month">
          <input type="text" :value="rightMonthLabel" readonly="readonly" style="cursor: pointer;">
        </div>
      </div>
      <ul class="cal-week">
        <li><b>日</b></li>
        <li>一</li>
        <li>二</li>
        <li>三</li>
        <li>四</li>
        <li>五</li>
        <li><b>六</b></li>
      </ul>
      <div class="cal-cm" style="height: 115px;">
        <div
          v-for="(day, index) in rightDays"
          :key="'right-' + index"
          class="cell"
          :style="{ left: day.left + 'px', top: day.top + 'px', cursor: day.enabled ? 'pointer' : 'default' }"
          @click="day.enabled && selectDate(day.date)"
          :class="{ 'disabled': !day.enabled, 'selected': isSelected(day.date) }"
        >
          <div class="so" :style="{ color: getDayColor(day) }">
            {{ day.text }}
          </div>
        </div>
      </div>
    </div>

    <div class="cal-ft">
      <a href="javascript:void(0);" class="cal-btn" style="color: rgb(0, 0, 0);" @click="selectToday">今天</a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import dayjs from 'dayjs'

const props = defineProps({
  visible: Boolean,
  top: { type: Number, default: 0 },
  left: { type: Number, default: 0 },
  selectedDate: { type: String, default: '' }
})

const emit = defineEmits(['select', 'close'])

const currentMonthDate = ref(dayjs()) // The first day of the month shown in the left calendar

// Initialize with selected date or today
watch(() => props.visible, (newVal) => {
  if (newVal) {
    if (props.selectedDate) {
      currentMonthDate.value = dayjs(props.selectedDate).startOf('month')
    } else {
      currentMonthDate.value = dayjs().startOf('month')
    }
  }
})

const leftYearLabel = computed(() => currentMonthDate.value.year())
const leftMonthLabel = computed(() => currentMonthDate.value.month() + 1 + '月')

const rightDate = computed(() => currentMonthDate.value.add(1, 'month'))
const rightYearLabel = computed(() => rightDate.value.year())
const rightMonthLabel = computed(() => rightDate.value.month() + 1 + '月')

const CELL_WIDTH = 38 // Increased from 32
const CELL_HEIGHT = 18 // Reduced from 22
const COL_WIDTH = 38
const COL_OFFSETS = [0, 38, 76, 114, 152, 190, 228]
const ROW_HEIGHT = 18

const generateDays = (monthDate) => {
  const days = []
  const startOfMonth = monthDate.startOf('month')
  const endOfMonth = monthDate.endOf('month')
  const startDayOfWeek = startOfMonth.day() // 0 (Sunday) to 6 (Saturday)
  
  // We need to fill the grid.
  // The inline styles use absolute positioning.
  // We can calculate row and col for each day.
  
  for (let i = 1; i <= endOfMonth.date(); i++) {
    const date = startOfMonth.date(i)
    const dayOfWeek = date.day()
    // Calculate row index.
    // The first day is at index `startDayOfWeek`.
    // The total index in the grid is `startDayOfWeek + i - 1`.
    const gridIndex = startDayOfWeek + i - 1
    const row = Math.floor(gridIndex / 7)
    const col = gridIndex % 7
    
    const top = 5 + row * ROW_HEIGHT
    const left = COL_OFFSETS[col]
    
    const isToday = date.isSame(dayjs(), 'day')
    const isPast = date.isBefore(dayjs(), 'day')
    
    days.push({
      date: date.format('YYYY-MM-DD'),
      text: isToday ? '今天' : i,
      top,
      left,
      enabled: !isPast, // Disable past dates? Usually yes for ticket booking.
      isToday
    })
  }
  return days
}

const leftDays = computed(() => generateDays(currentMonthDate.value))
const rightDays = computed(() => generateDays(rightDate.value))

const prevMonth = () => {
  currentMonthDate.value = currentMonthDate.value.subtract(1, 'month')
}

const nextMonth = () => {
  currentMonthDate.value = currentMonthDate.value.add(1, 'month')
}

const prevYear = () => {
  currentMonthDate.value = currentMonthDate.value.subtract(1, 'year')
}

const nextYear = () => {
  currentMonthDate.value = currentMonthDate.value.add(1, 'year')
}

const selectDate = (date) => {
  emit('select', date)
  emit('close')
}

const selectToday = () => {
  selectDate(dayjs().format('YYYY-MM-DD'))
}

const isSelected = (date) => {
  return props.selectedDate === date
}

const getDayColor = (day) => {
  if (!day.enabled) return '#ccc'
  // if (isSelected(day.date)) return '#fff' // Removed white text for selected
  // if (day.isToday) return '#fff' 
  
  if (day.text === '今天') return 'rgb(198, 11, 2)'
  
  // Weekends might be red?
  const d = dayjs(day.date)
  if (d.day() === 0 || d.day() === 6) return 'rgb(198, 11, 2)'
  
  return '#333'
}

// Close on click outside is handled by the parent or a global listener usually,
// but here we have @mousedown.prevent on the container to prevent closing when clicking inside.
// The parent needs to handle closing when clicking outside.
</script>

<style scoped>
.cal-wrap {
  width: 560px; /* Increased from 500px */
  background: #fff;
  border: 1px solid #298cba;
  padding: 5px 5px 30px 5px; /* Added bottom padding for absolute footer */
  box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
  font-family: 'Microsoft YaHei', sans-serif;
  font-size: 12px;
}

.cal {
  width: 270px; /* Increased from 240px */
  float: left;
  position: relative;
}

.cal-right {
  margin-left: 5px;
  border-left: 1px solid #ddd;
  padding-left: 5px;
}

.cal-top {
  height: 30px;
  position: relative;
  margin-bottom: 5px;
}

.cal-top a {
  width: 16px;
  height: 16px;
  position: absolute;
  top: 5px;
  cursor: pointer;
  background-image: url('@/assets/images/cal_btn.png'); /* Need to check if this asset exists or use CSS shapes */
}
/* Since I don't have the image, I'll use CSS arrows or characters for now */
.cal-top a.first { left: 0; background-position: 0 0; } /* << */
.cal-top a.prev { left: 20px; background-position: -16px 0; } /* < */
.cal-top a.next { right: 20px; background-position: -32px 0; } /* > */
.cal-top a.last { right: 0; background-position: -48px 0; } /* >> */

/* Fallback for missing image using pseudo-elements */
.cal-top a::before {
  content: '';
  display: block;
  width: 100%;
  height: 100%;
  text-align: center;
  line-height: 16px;
  font-weight: bold;
  color: #298cba;
}
.cal-top a.first::before { content: '«'; }
.cal-top a.prev::before { content: '‹'; }
.cal-top a.next::before { content: '›'; }
.cal-top a.last::before { content: '»'; }


.cal-top .month, .cal-top .year {
  float: left;
  margin-left: 45px;
  position: relative;
}
.cal-top .year { margin-left: 10px; }

.cal-right .cal-top .year { margin-left: 45px; }
.cal-right .cal-top .month { margin-left: 10px; }


.cal-top input {
  width: 60px;
  height: 20px;
  border: none;
  text-align: center;
  font-weight: normal;
  font-size: 14px;
  color: #333;
}

.cal-week {
  height: 20px; /* Reduced from 24px */
  background: #e9f3f8;
  border-top: 1px solid #b3d7e6;
  border-bottom: 1px solid #b3d7e6;
  padding: 0;
  margin: 0;
  list-style: none;
}

.cal-week li {
  float: left;
  width: 38px; /* Increased from 32px */
  height: 20px;
  line-height: 20px;
  text-align: center;
  color: #333;
}
/* Removed specific widths */


.cal-cm {
  position: relative;
  margin-top: 5px;
}

.cell {
  position: absolute;
  width: 38px; /* Increased from 32px */
  height: 18px; /* Reduced from 20px */
  text-align: center;
  line-height: 18px;
}

.cell .so {
  font-family: Arial, sans-serif;
  font-weight: bold;
}

.cell:hover {
  background: #dceeff;
  border: 1px solid #a5b9da;
  top: calc(var(--top) - 1px); /* Adjust for border? No, box-sizing */
  box-sizing: border-box;
}

.cell.selected {
  background: rgb(193, 217, 255);
  color: #333 !important;
  border: 1px solid rgb(165, 185, 218);
}

.cell.selected .so {
  color: #333 !important;
}

.cell.disabled {
  color: #ccc;
  cursor: default;
}
.cell.disabled:hover {
  background: none;
  border: none;
}

.cal-ft {
  position: absolute;
  right: 10px;
  bottom: 5px;
  border-top: none;
}

.cal-btn {
  display: inline-block;
  padding: 2px 5px;
  background: transparent;
  border: none;
  text-decoration: none;
  cursor: pointer;
  font-weight: bold;
}
</style>
