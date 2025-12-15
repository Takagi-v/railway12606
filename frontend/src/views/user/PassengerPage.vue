<template>
  <div class="passenger-page-content">
    <div class="order-panel">
      <!-- Search Form -->
          <div class="search-form-mini">
            <div class="form-item">
              <input 
                type="text" 
                class="input-txt" 
                v-model="query.name" 
                placeholder="请输入乘客姓名"
                style="width: 200px; margin-right: 0;"
              />
              <a href="javascript:;" class="btn-primary" @click="applyFilter" style="padding: 0 15px; margin-left: 10px; height: 30px; line-height: 30px; border-radius: 4px;">查询</a>
            </div>
          </div>

          <!-- Table Header -->
          <table class="order-panel-head">
            <colgroup>
              <col class="col-num" style="width: 60px;">
              <col class="col-name" style="width: 100px;">
              <col class="col-cardtype" style="width: 120px;">
              <col class="col-cardnum" style="width: 160px;">
              <col class="col-tel" style="width: 140px;">
              <col class="col-state" style="width: 80px;">
              <col class="col-op" style="width: 120px;">
            </colgroup>
            <tbody>
              <tr>
                <th>序号</th>
                <th>姓名</th>
                <th>证件类型</th>
                <th>证件号码</th>
                <th>手机／电话</th>
                <th>核验状态</th>
                <th>操作</th>
              </tr>
            </tbody>
          </table>

          <!-- List Container -->
          <div class="order-item">
            <div class="order-item-hd">
              <div class="order-hd-info">
                <a href="javascript:void(0);" id='add_contact' @click="openCreate">
                  <i class="icon icon-add-fill txt-success mr-sm"></i>添加
                </a>
              </div>
              <div class="order-hd-info" id='batch_del'>
                <a href="javascript:void(0);" @click="batchDelete">
                  <i class="icon icon-del txt-error mr-sm"></i>批量删除
                </a>
              </div>
            </div>
            
            <div class="order-item-bd">
              <table class="order-item-table">
                <colgroup>
                  <col class="col-num" style="width: 60px;">
                  <col class="col-name" style="width: 100px;">
                  <col class="col-cardtype" style="width: 120px;">
                  <col class="col-cardnum" style="width: 160px;">
                  <col class="col-tel" style="width: 140px;">
                  <col class="col-state" style="width: 80px;">
                  <col class="col-op" style="width: 120px;">
                </colgroup>
                <tbody>
                  <tr v-for="(p, idx) in filteredPassengers" :key="p.id">
                    <td>
                      <label class="check-inline">
                        <input 
                          type="checkbox" 
                          :value="p.id" 
                          v-model="selectedIds" 
                          :disabled="p.isDefault"
                        />
                        {{ idx + 1 }}
                      </label>
                    </td>
                    <td class="br-none">
                      <div class="name-yichu" :title="p.name">
                        {{ p.name }}
                        <span v-if="p.isDefault" class="badge badge-default" style="margin-left:5px;font-size:12px;background:#3B99FC;color:#fff;padding:1px 3px;border-radius:2px;">本人</span>
                      </div>
                    </td>
                    <td class="br-none">
                      <div>{{ p.idTypeLabel }}</div>
                    </td>
                    <td class="br-none">
                      <div>{{ p.idNoMasked }}</div>
                    </td>
                    <td class="br-none">
                      <div>{{ p.phoneMasked || '--' }}</div>
                    </td>
                    <td class="br-none">
                      <div class="verification-status-box">
                        <!-- ID Verification -->
                        <span 
                          class="verification-status-common verification-status-user"
                          :class="p.status === '正常' ? 'user-check-success' : 'user-check-error'"
                          :title="p.status === '正常' ? '已通过' : '待核验'"
                        ></span>
                        
                        <!-- Phone Verification (if phone exists) -->
                        <span 
                          v-if="p.phone"
                          class="verification-status-common verification-status-phone"
                          :class="p.phoneVerified === 'Y' ? 'mobile-check-success' : 'mobile-check-error'"
                          :title="p.phoneVerified === 'Y' ? '手机核验通过' : '手机核验未通过'"
                        ></span>
                      </div>
                    </td>
                    <td class="br-none">
                      <div class="list-operation">
                        <a v-if="!p.isDefault" href="javascript:void(0);" class="one-del" @click="handleDelete(p)">
                          <i class="icon icon-del"></i>
                        </a>
                        <a v-if="!p.isDefault" href="javascript:void(0);" class="one-edit" @click="openEdit(p)">
                          <i class="icon icon-edit"></i>
                        </a>
                        <span v-if="p.isDefault" style="color:#999;font-size:12px;">默认乘客</span>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="filteredPassengers.length === 0">
                    <td colspan="7" class="empty" style="padding: 50px 0; color: #999;">暂无乘车人</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <!-- Pagination -->
          <div class="pagination" v-if="totalPages > 1" style="margin-top: 20px; text-align: center;">
            <a
              href="javascript:;"
              class="page-btn"
              :class="{ disabled: currentPage === 1 }"
              @click="prevPage"
              style="margin-right: 10px;"
            >上一页</a>
            <span class="page-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
            <a
              href="javascript:;"
              class="page-btn"
              :class="{ disabled: currentPage === totalPages }"
              @click="nextPage"
              style="margin-left: 10px;"
            >下一页</a>
          </div>
        </div>

        <!-- Add/Edit Modal -->
        <a-modal
          v-model:open="showForm"
          :title="formMode === 'create' ? '新增乘车人' : '编辑乘车人'"
          :maskClosable="false"
          :footer="null"
          width="600px"
        >
          <a-form :model="form" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }" class="form-railway">
            <a-form-item label="姓名" required>
              <a-input v-model:value="form.name" placeholder="请输入姓名" />
            </a-form-item>
            <a-form-item label="证件类型" required>
              <a-select v-model:value="form.id_type">
                <a-select-option v-for="opt in idTypeOptions" :key="opt" :value="opt">
                  {{ opt }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item label="证件号码" required>
              <a-input v-model:value="form.id_number" placeholder="请输入证件号码" />
            </a-form-item>
            <a-form-item label="手机号" required>
              <a-input v-model:value="form.phone" placeholder="请输入手机号" />
            </a-form-item>
            <a-form-item label="旅客类型" required>
              <a-select v-model:value="form.passenger_type">
                <a-select-option v-for="opt in passengerTypeOptions" :key="opt" :value="opt">
                  {{ opt }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <div class="modal-footer" style="text-align: right; border-top: 1px solid #e8e8e8; padding-top: 10px; margin-top: 20px;">
              <a-button @click="closeForm" style="margin-right: 10px;">取消</a-button>
              <a-button type="primary" @click="submitForm" style="background: #FF8200; border-color: #FF8200;">确定</a-button>
            </div>
          </a-form>
        </a-modal>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getPassengers, createPassenger, updatePassenger, deletePassenger, syncDefaultPassenger, batchDeletePassengers } from '@/api/passenger'
// Import 12306 styles
import '@/assets/12306-passenger/center.css'
import '@/assets/12306-passenger/ticket_public_v70001.css'
import '@/assets/12306-passenger/passenger-custom.css'

// ... rest of script ...


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

const maskId = (id) => {
  if (!id || id.length < 10) return id
  return id.substring(0, 4) + '**********' + id.substring(id.length - 3)
}

const maskPhone = (phone) => {
  if (!phone || phone.length < 7) return phone
  // 12306 format: (+86)151****3156 or just 151****3156 if no country code
  // Assuming standard 11 digit mobile for now
  return '(+86)' + phone.substring(0, 3) + '****' + phone.substring(7)
}

const mapPassenger = p => ({
  id: p.id,
  name: p.name,
  type: p.passenger_type,
  idTypeLabel: p.id_type,
  idNo: p.id_number,
  idNoMasked: maskId(p.id_number),
  phone: p.phone,
  phoneMasked: maskPhone(p.phone),
  phoneVerified: p.verified ? 'Y' : 'N',
  status: p.verified ? '正常' : '待核验',
  isDefault: p.is_default || false
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

const syncDefault = async () => {
  try {
    await syncDefaultPassenger()
  } catch (e) {
    console.warn('同步默认乘客失败:', e)
    // Don't show error to user, just log it
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
  const v = form.value
  const phoneOk = /^\d{11}$/.test(String(v.phone || ''))
  const nameOk = String(v.name || '').trim().length >= 2
  const idTypeOk = !!v.id_type
  const idNoOk = String(v.id_number || '').trim().length > 0
  const pTypeOk = !!v.passenger_type
  if (!nameOk) {
    message.error('请填写有效的姓名')
    return
  }
  if (!idTypeOk) {
    message.error('请选择证件类型')
    return
  }
  if (!idNoOk) {
    message.error('请填写证件号码')
    return
  }
  if (!phoneOk) {
    message.error('请填写11位手机号')
    return
  }
  if (!pTypeOk) {
    message.error('请选择旅客类型')
    return
  }
  const dup = passengers.value.some(p => {
    if (formMode.value === 'edit' && p.id === editingId.value) return false
    return String(p.idNo) === String(v.id_number) && String(p.idTypeLabel) === String(v.id_type)
  })
  if (dup) {
    message.error('该证件号的乘车人已存在')
    return
  }
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
    const res = await batchDeletePassengers(selectedIds.value)
    if (res.code === 200) {
      message.success('批量删除成功')
      selectedIds.value = []
      allChecked.value = false
      await loadPassengers()
    }
  } catch (e) {
    // 错误信息由 request.js 拦截器统一处理
  }
}

const toggleAll = () => {
  if (allChecked.value) {
    // Only select non-default passengers
    selectedIds.value = filteredPassengers.value
      .filter(p => !p.isDefault)
      .map(p => p.id)
  } else {
    selectedIds.value = []
  }
}

onMounted(async () => {
  await syncDefault() // Sync default passenger first
  await loadPassengers()
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
.col-name .badge-default {
  margin-left: 8px;
  background: var(--primary-color);
  color: #fff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}
.default-row {
  background-color: #f0f7ff;
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
.action.disabled {
  color: #bbb;
  cursor: not-allowed;
  pointer-events: none;
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
