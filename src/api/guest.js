import request from '@/utils/request'

export function search_guest(data) {
    console.log('in search fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/guest/search',
        method: 'post',
        data
    })
}

export function add_guest(data) {
    console.log('in add fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/guest/add',
        method: 'post',
        data
    })
}

export function delete_guest(data) {
    console.log('in delete fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/guest/delete',
        method: 'post',
        data
    })
}

export function update_guest(data) {
    console.log('in search fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/guest/update',
        method: 'post',
        data
    })
}