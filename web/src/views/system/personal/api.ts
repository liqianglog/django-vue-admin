import { request } from '/@/utils/service';
import { PageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';
export function GetUserInfo(query: PageQuery) {
    return request({
        url: '/api/system/user/user_info/',
        method: 'get',
        params: query
    });
}


/**
 * 更新用户信息
 * @param data
 */
export function updateUserInfo(data: AddReq) {
    return request({
        url: '/api/system/user/update_user_info/',
        method: 'put',
        data: data
    })
}
