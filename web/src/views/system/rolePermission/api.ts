import { request } from "/@/utils/service";

export function getMenu(params:any) {
    return request({
        url: '/api/system/menu/',
        method: 'get',
        params:params
    });
}
