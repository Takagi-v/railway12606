<template>
  <div class="passenger-page">
    <a-form :model="query" layout="inline" class="filter form-railway">
      <a-form-item>
        <a-input
          v-model:value="query.name"
          placeholder="请输入乘客姓名"
          allow-clear
          style="width: 240px"
        />
      </a-form-item>
      <a-form-item>
        <a-button class="btn-query" @click="applyFilter">查询</a-button>
      </a-form-item>
    </a-form>

    <div class="list">
      <div class="list-actions">
        <a href="javascript:;" class="list-action add" @click="openCreate">
          <i class="icon icon-add-circle"></i>
          添加
        </a>
        <a
          href="javascript:;"
          class="list-action del"
          :class="{ disabled: selectedIds.length === 0 }"
          @click="batchDelete"
        >
          <i class="icon icon-del"></i>
          批量删除
        </a>
      </div>
      <table class="table" cellspacing="0" cellpadding="0">
        <thead>
          <tr>
            <th class="col-select">
              <input type="checkbox" v-model="allChecked" @change="toggleAll" />
            </th>
            <th class="col-index">序号</th>
            <th class="col-name">姓名</th>
            <th class="col-type">旅客类型</th>
            <th class="col-idtype">证件类型</th>
            <th class="col-idno">证件号码</th>
            <th class="col-phone">手机核验</th>
            <th class="col-status">状态</th>
            <th class="col-actions">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(p, idx) in filteredPassengers" :key="p.id">
            <td class="col-select">
              <input type="checkbox" :value="p.id" v-model="selectedIds" />
            </td>
            <td class="col-index">{{ idx + 1 }}</td>
            <td class="col-name">
              <i class="icon icon-person"></i>
              <span class="text">{{ p.name }}</span>
            </td>
            <td class="col-type">{{ p.type }}</td>
            <td class="col-idtype">{{ p.idTypeLabel }}</td>
            <td class="col-idno">{{ p.idNo }}</td>
            <td class="col-phone">
              <span :class="['badge', p.phoneVerified === 'Y' ? 'badge-success' : 'badge-warning']">
                {{ p.phoneVerified === 'Y' ? '已核验' : '未核验' }}
              </span>
            </td>
            <td class="col-status">{{ p.status }}</td>
            <td class="col-actions">
              <a href="javascript:;" class="action" @click="openEdit(p)">
                <i class="icon icon-edit"></i>
                编辑
              </a>
              <a href="javascript:;" class="action" @click="handleDelete(p)">
                <i class="icon icon-del"></i>
                删除
              </a>
            </td>
          </tr>
          <tr v-if="filteredPassengers.length === 0">
            <td colspan="8" class="empty">暂无乘车人</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <a
        href="javascript:;"
        class="page-btn"
        :class="{ disabled: currentPage === 1 }"
        @click="prevPage"
      >
        上一页
      </a>
      <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
      <a
        href="javascript:;"
        class="page-btn"
        :class="{ disabled: currentPage === totalPages }"
        @click="nextPage"
      >
        下一页
      </a>
    </div>
  </div>
  <a-modal
    v-model:open="showForm"
    :title="formMode === 'create' ? '新增乘车人' : '编辑乘车人'"
    :maskClosable="false"
    :footer="null"
  >
    <a-form :model="form" layout="vertical" class="form-railway">
      <a-form-item label="姓名">
        <a-input v-model:value="form.name" />
      </a-form-item>
      <a-form-item label="证件类型">
        <a-select v-model:value="form.id_type" style="width: 100%">
          <a-select-option v-for="opt in idTypeOptions" :key="opt" :value="opt">
            {{ opt }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <a-form-item label="证件号码">
        <a-input v-model:value="form.id_number" />
      </a-form-item>
      <a-form-item label="手机号">
        <a-input v-model:value="form.phone" />
      </a-form-item>
      <a-form-item label="旅客类型">
        <a-select v-model:value="form.passenger_type" style="width: 100%">
          <a-select-option v-for="opt in passengerTypeOptions" :key="opt" :value="opt">
            {{ opt }}
          </a-select-option>
        </a-select>
      </a-form-item>
      <div class="modal-footer">
        <a-button @click="closeForm">取消</a-button>
        <a-button type="primary" @click="submitForm">确定</a-button>
      </div>
    </a-form>
  </a-modal>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getPassengers, createPassenger, updatePassenger, deletePassenger } from '@/api/passenger'

const query = ref({ name: '' })
const loading = ref(false)

const passengers = ref([])
const selectedIds = ref([])
const allChecked = ref(false)

const idTypeOptions = ['身份证', '港澳通行证', '台胞证', '护照']
const passengerTypeOptions = ['成人', '学生', '儿童']

const showForm = ref(false)
const formMode = ref('create')
const editingId = ref(null)
const form = ref({ name: '', id_type: '身份证', id_number: '', phone: '', passenger_type: '成人' })

const pageSize = 10
const currentPage = ref(1)

const filteredPassengersAll = computed(() => {
  const q = query.value
  return passengers.value.filter(p => {
    if (q.name && !String(p.name).includes(q.name)) return false
    return true
  })
})

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredPassengersAll.value.length / pageSize))
)
const filteredPassengers = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredPassengersAll.value.slice(start, end)
})

const applyFilter = () => {
  currentPage.value = 1
}
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value -= 1
}
const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value += 1
}

const mapPassenger = p => ({
  id: p.id,
  name: p.name,
  type: p.passenger_type,
  idTypeLabel: p.id_type,
  idNo: p.id_number,
  phone: p.phone,
  phoneVerified: p.verified ? 'Y' : 'N',
  status: p.verified ? '正常' : '待核验'
})

const loadPassengers = async () => {
  loading.value = true
  try {
    const res = await getPassengers()
    if (res.code === 200) {
      passengers.value = (res.data || []).map(mapPassenger)
    }
  } catch (e) {
    message.error('查询失败')
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  formMode.value = 'create'
  editingId.value = null
  form.value = { name: '', id_type: '身份证', id_number: '', phone: '', passenger_type: '成人' }
  showForm.value = true
}

const openEdit = p => {
  formMode.value = 'edit'
  editingId.value = p.id
  form.value = {
    name: p.name,
    id_type: p.idTypeLabel,
    id_number: p.idNo,
    phone: p.phone || '',
    passenger_type: p.type
  }
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
}

const submitForm = async () => {
  try {
    if (formMode.value === 'create') {
      const res = await createPassenger(form.value)
      if (res.code === 200 || res.code === 201) {
        message.success('添加成功')
        showForm.value = false
        await loadPassengers()
      }
    } else if (editingId.value) {
      const res = await updatePassenger(editingId.value, form.value)
      if (res.code === 200) {
        message.success('修改成功')
        showForm.value = false
        await loadPassengers()
      }
    }
  } catch (e) {
    message.error('保存失败')
  }
}

const handleDelete = async p => {
  try {
    const res = await deletePassenger(p.id)
    if (res.code === 200) {
      message.success('删除成功')
      await loadPassengers()
    }
  } catch (e) {
    message.error('删除失败')
  }
}

const batchDelete = async () => {
  if (selectedIds.value.length === 0) return
  try {
    await Promise.all(selectedIds.value.map(id => deletePassenger(id)))
    message.success('批量删除成功')
    selectedIds.value = []
    allChecked.value = false
    await loadPassengers()
  } catch (e) {
    message.error('批量删除失败')
  }
}

const toggleAll = () => {
  if (allChecked.value) {
    selectedIds.value = filteredPassengers.value.map(p => p.id)
  } else {
    selectedIds.value = []
  }
}

onMounted(() => {
  loadPassengers()
})
</script>

<style scoped>
.passenger-page :global(.header a) {
  text-decoration: none !important;
}
.passenger-page :global(.header a:hover) {
  text-decoration: none !important;
}
.passenger-page :global(.header .header-menu a) {
  text-decoration: none !important;
}
.passenger-page :global(.header .nav-hd) {
  color: #fff;
  font-size: 14px;
  line-height: 40px;
}
.passenger-page :global(.header .nav-item.active .nav-hd) {
  font-weight: 600 !important;
}
.passenger-page :global(.header .menu-nav-hd) {
  font-size: 14px;
}
.passenger-page {
  padding: var(--spacing-sm);
}
.toolbar {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: var(--spacing-sm);
}
.toolbar-left,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  font-size: var(--font-size-xs);
  border-radius: var(--border-radius-small);
  text-decoration: none;
  cursor: pointer;
}
.btn-primary {
  background: var(--primary-color);
  color: var(--text-color-inverse);
}
.btn-danger {
  background: var(--error-color);
  color: var(--text-color-inverse);
}
.btn-default {
  background: var(--background-color-light);
  color: var(--text-color);
  border: 1px solid var(--border-color-light);
}
.btn.disabled {
  opacity: 0.5;
  pointer-events: none;
}
.filter {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  background: var(--background-color-light);
  border: 1px solid var(--border-color-light);
  border-radius: var(--border-radius-small);
  padding: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}
.filter-item {
  display: contents;
}
.filter-item label {
  font-size: var(--font-size-xs);
  color: var(--text-color-secondary);
}
.input,
.select {
  height: 28px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-small);
  padding: 0 var(--spacing-xs);
  font-size: var(--font-size-xs);
}
.list {
  background: var(--background-color-light);
  border: 1px solid var(--border-color-light);
  border-radius: var(--border-radius-small);
}
.list-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #e6f7ff;
  border-bottom: 1px solid var(--border-color-light);
  padding: 8px 12px;
}
.list-action {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #3b99fc;
  text-decoration: none;
}
.list-action.add .icon {
  color: #52c41a;
}
.list-action.del .icon {
  color: #ff4d4f;
}
.list-action.disabled {
  color: #bbb;
  pointer-events: none;
}
.table {
  width: 100%;
  border-collapse: collapse;
}
.table thead th {
  background: var(--background-color-dark);
  color: var(--text-color-secondary);
  font-weight: 500;
  font-size: var(--font-size-xs);
  padding: 10px var(--spacing-xs);
  border-bottom: 1px solid var(--border-color-light);
  text-align: center;
}
.table tbody td {
  padding: 10px var(--spacing-xs);
  font-size: var(--font-size-xs);
  color: var(--text-color);
  border-bottom: 1px solid var(--border-color-light);
}
.col-select {
  width: 36px;
}
.col-index {
  width: 56px;
}
.col-name {
  width: 160px;
}
.col-type {
  width: 100px;
}
.col-idtype {
  width: 140px;
}
.col-idno {
  width: 200px;
}
.col-phone {
  width: 120px;
}
.col-status {
  width: 80px;
}
.col-actions {
  width: 160px;
}
.col-name .icon {
  margin-right: 6px;
  font-size: 16px;
  color: var(--primary-color);
}
.badge {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: var(--font-size-xs);
}
.badge-success {
  background: var(--background-color-dark);
  color: var(--primary-color);
}
.badge-warning {
  background: #fff7e6;
  color: var(--warning-color);
}
.action {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--primary-color);
  text-decoration: none;
  margin-right: 12px;
}
.action .icon {
  font-size: 14px;
}
.empty {
  text-align: center;
  color: var(--text-color-secondary);
  padding: 24px 0;
}
.pagination {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  justify-content: flex-end;
  margin-top: var(--spacing-sm);
}
.page-btn {
  color: var(--primary-color);
  text-decoration: none;
}
.page-btn.disabled {
  color: #bbb;
  pointer-events: none;
}
.page-info {
  color: var(--text-color-secondary);
  font-size: var(--font-size-xs);
}

.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal {
  width: 520px;
  background: var(--background-color-light);
  border-radius: var(--border-radius-small);
  box-shadow: var(--shadow-medium);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border-color-light);
  font-size: var(--font-size-sm);
}
.modal-close {
  color: var(--text-color-secondary);
  text-decoration: none;
}
.modal-body {
  padding: var(--spacing-sm);
}
.form-row {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 8px;
  align-items: center;
  margin-bottom: 10px;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  padding: 10px 12px;
  border-top: 1px solid var(--border-color-light);
}
</style>
.btn-query.ant-btn { background: #fff; color: #333; border: 1px solid #d9d9d9; }
.btn-query.ant-btn:hover { color: var(--primary-color); border-color: var(--primary-color); }
