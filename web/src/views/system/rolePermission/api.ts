import { request } from "/@/utils/service";

/**
 * 获取角色所拥有的菜单
 * @param params
 */
export function GetMenu(params:any) {
    return request({
        url: '/api/system/role_menu_button_permission/role_get_menu/',
        method: 'get',
        params:params
    });
}

/***
 * 新增权限
 * @param data
 * @constructor
 */
export function SaveMenuPermission(data:any) {
    return request({
        url: '/api/system/role_menu_permission/save_auth/',
        method: 'post',
        data:data
    });
}


/**
 * 获取菜单下的按钮
 * @param params
 * @constructor
 */
export function GetMenuButton(params:any) {
    return request({
        url: '/api/system/role_menu_button_permission/role_menu_get_button/',
        method: 'get',
        params:params
    });
}





/***
 * 根据角色获取数据权限范围
 * @constructor
 */
export function GetDataScope (params:any={}) {
    return request({
        url: '/api/system/role_menu_button_permission/data_scope/',
        method: 'get',
        params: params
    })
}

/***
 * 获取权限部门
 * @constructor
 */
export function GetDataScopeDept (params:any) {
    return request({
        url: '/api/system/role_menu_button_permission/role_to_dept_all/',
        method: 'get',
        params: params
    })
}

/***
 * 新增权限
 * @param data
 * @constructor
 */
export function CreatePermission(data:any) {
    return request({
        url: '/api/system/role_menu_button_permission/',
        method: 'post',
        data:data
    });
}

/***
 * 根据菜单获取菜单下按钮
 * @param params
 */
export function getObj(params:any) {
    return request({
        url: '/api/system/role_menu_button_permission/menu_to_button/',
        method: 'get',
        params:params
    });
}

/**
 * 删除按钮权限
 * @param data
 * @constructor
 */
export function DeletePermission(data:any) {
    return request({
        url: `/api/system/role_menu_button_permission/${data.id}/`,
        method: 'delete',
        data:{}
    });
}

