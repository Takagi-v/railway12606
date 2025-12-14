/**
 * Passenger API
 * 乘客管理API
 */
import request from '@/utils/request'

/**
 * 获取乘客列表
 */
export const getPassengers = () => {
  return request({
    url: '/passengers',
    method: 'get'
  })
}

/**
 * 同步/创建默认乘客（用户本人）
 */
export const syncDefaultPassenger = () => {
  return request({
    url: '/passengers/sync-default',
    method: 'post'
  })
}

/**
 * 添加乘客
 */
export const createPassenger = data => {
  return request({
    url: '/passengers',
    method: 'post',
    data
  })
}

/**
 * 编辑乘客
 */
export const updatePassenger = (id, data) => {
  return request({
    url: `/passengers/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除乘客
 */
/**
 * 删除乘客
 */
export const deletePassenger = id => {
  return request({
    url: `/passengers/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除乘客
 */
export const batchDeletePassengers = ids => {
  return request({
    url: '/passengers/batch-delete',
    method: 'post',
    data: ids
  })
}
