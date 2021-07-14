import request from '@/utils/request'

export function add_saving_account(data) {
    console.log('in add saving fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/add_saving',
        method: 'post',
        data
    })
}

export function add_checking_account(data) {
    console.log('in add checking fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/add_checking',
        method: 'post',
        data
    })
}

export function search_account(data) {
    console.log('in search account fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/search_account',
        method: 'post',
        data
    })
}

export function delete_account(data) {
    console.log('in delete account fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/delete_account',
        method: 'post',
        data
    })
}

export function get_account_info(data) {
    console.log('in get account info fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/get_account_info',
        method: 'post',
        data
    })
}

export function update_saving_account(data) {
    console.log('in update_saving_account fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/update_saving_account',
        method: 'post',
        data
    })
}

export function update_checking_account(data) {
    console.log('in update_checking_account fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/update_checking_account',
        method: 'post',
        data
    })
}

export function get_user_account_detail(data) {
    console.log('in account detail fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/account/get_account_detail',
        method: 'post',
        data
    })
}