/**
 * @description 校验是否为租户模式。租户模式把域名替换成 域名 加端口
 */
export const getBaseURL = function () {
    var baseURL = import.meta.env.VITE_API_URL as any
    var param = baseURL.split('/')[3] || ''
    if (window.pluginsAll && window.pluginsAll.indexOf('dvadmin-tenants-web') !== -1 && (!param || baseURL.startsWith('/'))) {
        // 1.把127.0.0.1 替换成和前端一样域名
        // 2.把 ip 地址替换成和前端一样域名
        // 3.把 /api 或其他类似的替换成和前端一样域名
        // document.domain
        var host = baseURL.split('/')[2]
        if (host) {
            var prot = baseURL.split(':')[2] || 80
            if (prot === 80 || prot === 443) {
                host = document.domain
            } else {
                host = document.domain + ':' + prot
            }
            baseURL = baseURL.split('/')[0] + '//' + baseURL.split('/')[1] + host + '/' + param
        } else {
            baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' : '') + location.port + baseURL
        }
    }
    if (!baseURL.endsWith('/')) {
        baseURL += '/'
    }
    return baseURL
}

export const getWsBaseURL = function () {
    let baseURL = import.meta.env.VITE_API_URL as any
    let param = baseURL.split('/')[3] || ''
    if (window.pluginsAll && window.pluginsAll.indexOf('dvadmin-tenants-web') !== -1 && (!param || baseURL.startsWith('/'))) {
        // 1.把127.0.0.1 替换成和前端一样域名
        // 2.把 ip 地址替换成和前端一样域名
        // 3.把 /api 或其他类似的替换成和前端一样域名
        // document.domain
        var host = baseURL.split('/')[2]
        if (host) {
            var prot = baseURL.split(':')[2] || 80
            if (prot === 80 || prot === 443) {
                host = document.domain
            } else {
                host = document.domain + ':' + prot
            }
            baseURL = baseURL.split('/')[0] + '//' + baseURL.split('/')[1] + host + '/' + param
        } else {
            baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' : '') + location.port + baseURL
        }
    } else if (param !== '' || baseURL.startsWith('/')) {
        baseURL = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.hostname + (location.port ? ':' : '') + location.port + baseURL
    }
    if (!baseURL.endsWith('/')) {
        baseURL += '/'
    }
    if (baseURL.startsWith('http')) { // https 也默认会被替换成 wss
        baseURL = baseURL.replace('http', 'ws')
    }
    return baseURL
}
