import request from '@/utils/request'

export function get_logfile(data) {
    console.log('in get logfile fuction')
    // console.log(data)
    return request({
        url: 'http://localhost:4444/statistics/get_logfile',
        method: 'post',
        data
    })
}

export function get_saving_record(data) {
    console.log('in get saving record fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/statistics/get_saving_record',
        method: 'post',
        data
    })
}

export function get_loan_record(data) {
    console.log('in get loan record fuction')
    console.log(data)
    return request({
        url: 'http://localhost:4444/statistics/get_loan_record',
        method: 'post',
        data
    })
}
