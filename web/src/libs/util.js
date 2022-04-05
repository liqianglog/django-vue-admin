import cookies from './util.cookies'
import db from './util.db'
import log from './util.log'
const util = {
  cookies,
  db,
  log
}

/**
 * @description 更新标题
 * @param {String} titleText 标题
 */
util.title = function (titleText) {
  const processTitle = process.env.VUE_APP_TITLE || 'D2Admin'
  window.document.title = `${processTitle}${titleText ? ` | ${titleText}` : ''}`
}

/**
 * @description 打开新页面
 * @param {String} url 地址
 */
util.open = function (url) {
  var a = document.createElement('a')
  a.setAttribute('href', url)
  a.setAttribute('target', '_blank')
  a.setAttribute('id', 'd2admin-link-temp')
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(document.getElementById('d2admin-link-temp'))
}
/**
 * @description 校验是否为租户模式。租户模式把域名替换成 域名 加端口
 */
util.baseURL = function () {
  var baseURL = process.env.VUE_APP_API
  if (window.pluginsAll && window.pluginsAll.indexOf('dvadmin-tenant') !== -1) {
    // document.domain
    var host = baseURL.split('/')[2]
    var prot = host.split(':')[1] || 80
    host = document.domain + ':' + prot
    baseURL = baseURL.split('/')[0] + '//' + baseURL.split('/')[1] + host + '/' + (baseURL.split('/')[3] || '')
  }
  if (!baseURL.endsWith('/')) {
    baseURL += '/'
  }
  return baseURL
}

export default util
