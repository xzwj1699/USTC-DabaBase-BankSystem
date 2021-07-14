import request from '@/utils/request'

export function login(data) {
  console.log('in login fuction')
  console.log(data)
  return request({
    url: 'http://localhost:4444/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  console.log('in get info function')
  return request({
    url: 'http://localhost:4444/user_info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-element-admin/user/logout',
    method: 'post'
  })
}
