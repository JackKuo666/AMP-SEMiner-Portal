// 整个项目api的统一管理

import request from './request'

// 请求首页左侧的表格数据

export default {
    getAllAmpsData(params) {
        return request({
            url: '/getAllAmps',
            method: 'get',
            data: params
        })
    },
    getPdbFile(params) {
        return request({
            url: '/getPdbFile',
            method: 'get',
            data: params
        })
    },
    getSeqProperties(params) {
        return request({
            url: '/getSeqProperties',
            method: 'get',
            data: params
        })
    },
    getProStruProperties(params) {
        return request({
            url: '/getProStruProperties',
            method: 'get',
            data: params
        })
    },
    getStruProperties(params) {
        return request({
            url: '/getStruProperties',
            method: 'get',
            data: params
        })
    },

}