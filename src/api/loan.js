import request from '@/utils/request'

export function add_loan(data) {
    console.log('in pay loan fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/loan/add',
        method: 'post',
        data
    })
}

export function get_loan_list(data) {
    console.log('in get loan list fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/loan/get_list',
        method: 'post',
        data
    })
}

export function add_pay_loan(data) {
    console.log('in get loan detail fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/loan/add_pay_loan',
        method: 'post',
        data
    })
}

export function get_loan_detail(data) {
    console.log('in add pay loan fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/loan/loan_detail',
        method: 'post',
        data
    })
}

export function delete_loan(data) {
    console.log('in add pay loan fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/loan/delete',
        method: 'post',
        data
    })
}

export function search_loan(data) {
    console.log('in add pay loan fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/loan/search',
        method: 'post',
        data
    })
}