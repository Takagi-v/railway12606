/**
 * Passenger API
 * 乘客管理API
 */
import request from './request'

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
export const deletePassenger = id => {
  return request({
    url: `/passengers/${id}`,
    method: 'delete'
  })
}
