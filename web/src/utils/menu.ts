import XEUtils from "xe-utils"

/**
 * @description: 处理后端菜单数据格式
 * @param {Array} menuData
 * @return {*}
 */
export const handleMenu = (menuData: Array<any>) => {
    // 先处理menu meta数据转换
    const handleMeta = (item: any) => {
        item.meta = {
            title: item.title,
            isLink: item.is_link,
            isHide: !item.visible,
            isKeepAlive: true,
            isAffix: false,
            isIframe: false,
            roles: ['admin'],
            icon: item.icon
        }
        item.name = item.component_name
        return item
    }
    menuData.forEach((val) => {
        handleMeta(val)
        val.path = val.web_path
    })

    const data = XEUtils.toArrayTree(menuData, {
        parentKey: 'parent',
        strict: true,
    })
    const menu = [
        {
            path: '/home', name: 'home', component: '/system/home/index', meta: {
                title: 'message.router.home',
                isLink: '',
                isHide: false,
                isKeepAlive: true,
                isAffix: true,
                isIframe: false,
                roles: ['admin'],
                icon: 'iconfont icon-shouye'
            }
        },
        ...data
    ]
    console.log(menu)
    return menu
}
