<template>
  <ul class="center-menu" ref="menuRef">
    <li v-for="g in menu" :key="g.key" class="menu-item">
      <h2
        class="menu-tit"
        :class="{ active: activeGroup === g.label, clickable: isClickableGroup(g.key) }"
        @click="onGroupClick(g)"
      >
        {{ g.label }}
        <i
          v-if="g.children && g.children.length"
          class="icon icon-switch"
          :class="{ open: expanded[g.key] }"
          @click.stop="toggleGroup(g.key)"
        ></i>
      </h2>
      <ul
        v-if="g.children && g.children.length"
        class="menu-sub"
        :style="{ display: expanded[g.key] ? 'block' : 'none' }"
      >
        <li v-for="it in g.children" :key="it.label + it.path" :class="{ active: isActive(it) }">
          <a href="javascript:;" @click.prevent="goItem(it)">{{ it.label }}</a>
        </li>
      </ul>
    </li>
  </ul>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { computed, reactive, ref, onMounted, watch, nextTick } from 'vue'

const props = defineProps({
  context: { type: String, default: 'user' }
})
const emit = defineEmits(['heightChange'])

const router = useRouter()
const route = useRoute()

const menu = [
  { key: 'center', label: '个人中心', children: [] },
  {
    key: 'orders',
    label: '订单中心',
    children: [
      { label: '火车票订单', path: '/user/orders' },
      { label: '候补订单', path: '/service/waitlist' },
      { label: '计次•定期票订单', path: '/service/railway-pass' },
      { label: '约号订单', path: '/service/railway-pass' },
      { label: '雪具快运订单', path: '/service/showcase' },
      { label: '餐饮•特产', path: '/service/showcase' },
      { label: '保险订单', path: '/service/feedback' },
      { label: '电子发票', path: '/announcement' }
    ]
  },
  { key: 'ticket-self', label: '本人车票', children: [] },
  { key: 'vip', label: '会员中心', children: [] },
  {
    key: 'profile',
    label: '个人信息',
    children: [
      { label: '查看个人信息', path: '/user/profile', query: { section: 'view' } },
      { label: '账号安全', path: '/user/profile', query: { section: 'security' } },
      { label: '手机核验', path: '/user/profile', query: { section: 'phone' } },
      { label: '账号注销', path: '/user/profile', query: { section: 'close' } }
    ]
  },
  {
    key: 'common',
    label: '常用信息管理',
    children: [
      { label: '乘车人', path: '/user/passengers' },
      { label: '地址管理', path: '/user/passengers', query: { tab: 'address' } }
    ]
  },
  {
    key: 'service',
    label: '温馨服务',
    children: [
      { label: '重点旅客预约', path: '/service/special-passenger' },
      { label: '遗失物品查找', path: '/service/lost-items' },
      { label: '服务查询', path: '/service/station-guide' }
    ]
  },
  {
    key: 'advice',
    label: '投诉和建议',
    children: [
      { label: '投诉', path: '/service/feedback' },
      { label: '建议', path: '/service/feedback' }
    ]
  }
]

const expanded = reactive({})
const menuRef = ref(null)

const ensureExpanded = () => {
  menu.forEach(m => {
    if (!(m.key in expanded))
      expanded[m.key] = ['orders', 'profile', 'common', 'service', 'advice'].includes(m.key)
  })
  const p = route.path || ''
  const found = menu.find(m => m.children && m.children.some(it => p.startsWith(it.path)))
  if (found) expanded[found.key] = true
}

ensureExpanded()

const isClickableGroup = key => ['center', 'ticket-self', 'vip'].includes(key)
const onGroupClick = g => {
  if (!isClickableGroup(g.key)) return
  if (g.key === 'center') {
    router.push({ path: '/user/profile', query: { group: '个人中心' } })
    return
  }
  if (g.key === 'ticket-self') {
    router.push({ path: '/service/railway-pass', query: { group: '本人车票' } })
    return
  }
  if (g.key === 'vip') {
    router.push({ path: '/service/railway-pass', query: { group: '会员中心' } })
    return
  }
}
const toggleGroup = key => {
  expanded[key] = !expanded[key]
}

const goItem = it => {
  const keep = ['火车票订单', '乘车人']
  if (props.context === 'service') {
    if (!keep.includes(it.label)) {
      router.push({ path: '/service/railway-pass', query: { menu: it.label } })
      return
    }
    router.push({ path: it.path, query: it.query || {} })
    return
  }
  const keepUser = ['火车票订单', '乘车人', '查看个人信息']
  if (!keepUser.includes(it.label)) {
    router.push({ path: '/service/railway-pass', query: { menu: it.label } })
    return
  }
  router.push({ path: it.path, query: it.query || {} })
}

const isActive = it => {
  const p = route.path || ''
  const q = route.query || {}
  if (props.context === 'service') {
    if (p === '/service/railway-pass' && q.group) return false
    if (p === '/service/railway-pass') return String(q.menu || '') === it.label
  } else {
    if ('group' in q) return false
  }
  if (p !== it.path) return false
  const expected = it.query || {}
  const keys = Object.keys(expected)
  if (!keys.length) {
    if ('tab' in q) return String(q.tab || '') === 'passengers'
    return true
  }
  return keys.every(k => String(q[k] || '') === String(expected[k] || ''))
}

const activeGroup = computed(() => {
  const q = route.query || {}
  if (q.group) return String(q.group || '')
  return ''
})

const emitHeight = () => {
  nextTick(() => {
    const el = menuRef.value
    if (!el) return
    emit('heightChange', el.offsetHeight)
  })
}

onMounted(() => {
  emitHeight()
  window.addEventListener('resize', emitHeight)
})

watch(
  () => route.fullPath,
  () => emitHeight()
)
watch(
  () => JSON.stringify(expanded),
  () => emitHeight()
)
</script>

<style scoped>
@import url('@/assets/12306-icons/fonts/iconfont.css');

.center-menu {
  width: 130px;
  background: transparent;
  border: none;
  list-style: none;
  padding: 0;
  margin: 0;
}
.center-menu .menu-item {
  margin-bottom: 4px;
}
.center-menu .menu-tit {
  height: 30px;
  line-height: 30px;
  font-size: 14px;
  color: #333;
  margin: 0;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: default;
  background-color: transparent;
}
.center-menu .menu-tit.clickable {
  cursor: pointer;
}
.center-menu .menu-tit.active {
  background: #3b99fc;
  color: #fff;
}
.center-menu .menu-tit .icon-switch {
  font-size: 16px;
  color: #ccc;
  cursor: pointer;
  transition: transform 0.2s;
}
.center-menu .menu-tit .icon-switch.open {
  transform: rotate(180deg);
}
.center-menu .menu-tit.active .icon-switch {
  color: #fff;
}
.center-menu .menu-sub {
  list-style: none;
  padding: 0;
  margin: 0;
}
.center-menu .menu-sub li a {
  display: block;
  height: 30px;
  line-height: 30px;
  padding: 0 10px 0 20px;
  color: #666;
  text-decoration: none;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.center-menu .menu-sub li a:hover {
  color: #3b99fc;
  text-decoration: none;
}
.center-menu .menu-sub li.active a {
  color: #3b99fc;
  text-decoration: none;
}
</style>
