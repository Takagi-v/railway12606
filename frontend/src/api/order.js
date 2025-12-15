/**
 * Order API
 * 订单管理API
 */
import request from '@/utils/request'

/**
 * 创建订单
 */
export const createOrder = data => {
  return request({
    url: '/orders/create',
    method: 'post',
    data
  })
}

/**
 * 获取订单列表
 */
export const getOrders = params => {
  return request({
    url: '/orders',
    method: 'get',
    params,
    paramsSerializer: params => {
      const searchParams = new URLSearchParams()
      Object.keys(params).forEach(key => {
        if (params[key] === undefined || params[key] === null) return
        if (Array.isArray(params[key])) {
          params[key].forEach(val => searchParams.append(key, val))
        } else {
          searchParams.append(key, params[key])
        }
      })
      return searchParams.toString()
    }
  })
}

/**
 * 获取订单详情
 */
export const getOrderDetail = orderId => {
  return request({
    url: `/orders/${orderId}`,
    method: 'get'
  })
}

/**
 * 支付订单
 */
export const payOrder = orderId => {
  return request({
    url: `/orders/${orderId}/pay`,
    method: 'post',
    data: {}
  })
}

/**
 * 取消订单
 */
export const cancelOrder = orderId => {
  return request({
    url: `/orders/${orderId}/cancel`,
    method: 'post',
    data: {}
  })
}

/**
 * 退票
 */
export const refundOrder = (orderId, data) => {
  return request({
    url: `/orders/${orderId}/refund`,
    method: 'post',
    data
  })
}
