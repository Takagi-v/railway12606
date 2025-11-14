/**
 * Train API
 * 车次查询API
 */
import request from "@/utils/request";

/**
 * 查询车次
 */
export const searchTrains = params => {
  return request({
<<<<<<< HEAD
    url: '/trains/search',
    method: 'get',
    params
  })
}
=======
    url: "/trains/search",
    method: "get",
    params,
  });
};
>>>>>>> origin/feature/user-authentication
