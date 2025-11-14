/**
 * Order API
 * 订单管理API
 */
import request from "@/utils/request";

/**
 * 创建订单
 */
export const createOrder = data => {
  return request({
    url: "/orders/create",
    method: "post",
    data,
  });
};

/**
 * 获取订单列表
 */
export const getOrders = params => {
  return request({
    url: "/orders",
    method: "get",
    params,
  });
};

/**
 * 获取订单详情
 */
export const getOrderDetail = orderId => {
  return request({
    url: `/orders/${orderId}`,
    method: "get",
  });
};

/**
 * 支付订单
 */
export const payOrder = orderId => {
  return request({
    url: `/orders/${orderId}/pay`,
    method: "post",
  });
};

/**
 * 取消订单
 */
export const cancelOrder = orderId => {
  return request({
    url: `/orders/${orderId}/cancel`,
    method: "post",
  });
};

/**
 * 退票
 */
export const refundOrder = (orderId, data) => {
  return request({
    url: `/orders/${orderId}/refund`,
<<<<<<< HEAD
    method: 'post',
    data
  })
}
=======
    method: "post",
    data,
  });
};
>>>>>>> origin/feature/user-authentication
