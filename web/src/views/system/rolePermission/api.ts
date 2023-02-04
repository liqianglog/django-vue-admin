import { request } from "/@/utils/service";

/**
 * 获取角色所拥有的菜单
 * @param params
 */
export function GetMenu(params:any) {
    return request({
        url: '/api/system/role/role_get_menu/',
        method: 'get',
        params:params
    });
}


/***
 * 根据角色获取数据权限范围
 * @constructor
 */
export function GetDataScope () {
    return request({
        url: '/api/system/role/data_scope/',
        method: 'get',
        params: {}
    })
}

/***
 * 获取权限部门
 * @constructor
 */
export function GetDataScopeDept () {
    return request({
        url: '/api/system/role/data_scope_dept/',
        method: 'get',
        params: {}
    })
}
