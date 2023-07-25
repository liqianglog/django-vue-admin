import { request } from "/@/utils/service";

export function getCaptcha() {
    return request({
        url: '/api/captcha/',
        method: 'get',
    });
}
export function login(params: object) {
    return request({
        url: '/api/login/',
        method: 'post',
        data: params
    });
}
export function getUserInfo() {
    return request({
        url: '/api/system/user/user_info/',
        method: 'get',
    });
}
