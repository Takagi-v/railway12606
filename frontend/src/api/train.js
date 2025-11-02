/**
 * Train API
 * 车次查询API
 */
import request from './request'

/**
 * 查询车次
 */
export const searchTrains = params => {
  return request({
    url: '/trains/search',
    method: 'get',
    params
  })
}
