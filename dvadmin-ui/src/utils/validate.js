/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  const valid_map = ['admin', 'editor']
  return valid_map.indexOf(str.trim()) >= 0
}

/**
 * @param {string} url
 * @returns {Boolean}
 */
export function validURL(url) {
  const reg = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
  return reg.test(url)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validLowerCase(str) {
  const reg = /^[a-z]+$/
  return reg.test(str)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUpperCase(str) {
  const reg = /^[A-Z]+$/
  return reg.test(str)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validAlphabets(str) {
  const reg = /^[A-Za-z]+$/
  return reg.test(str)
}

/**
 * @param {string} email
 * @returns {Boolean}
 */
export function validEmail(email) {
  const reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return reg.test(email)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function isString(str) {
  if (typeof str === 'string' || str instanceof String) {
    return true
  }
  return false
}

/**
 * @param {Array} arg
 * @returns {Boolean}
 */
export function isArray(arg) {
  if (typeof Array.isArray === 'undefined') {
    return Object.prototype.toString.call(arg) === '[object Array]'
  }
  return Array.isArray(arg)
}

export function getCrontabData(val) {
  if (!val || Object.keys(val).length === 0) return '';
  const week = {1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'};
  let res = '';
  if (val.month_of_year !== '*') {
    res = `${val.month_of_year} 月 ${val.day_of_month} 日 ${val.hour}点${val.minute}分`;
  } else if (val.day_of_month !== '*') {
    res = `每月 ${val.day_of_month} 日 ${val.hour}点${val.minute}分`;
  } else if (val.day_of_week !== '*') {
    res = `每周周${week[val.day_of_week] || val.day_of_week} ${val.hour}点${val.minute}分 `;
  } else if (val.hour !== '*') {
    res = `每天 ${val.hour}点${val.minute}分`;
  } else if (val.minute !== '*') {
    res = `每分钟 ${val.minute}秒`;
  } else {
    res = `${val.month_of_year} 月 ${val.day_of_month} 日 ${val.hour}点${val.minute}分`;
  }
  return res.replace(/\*/g, '00');
}

export function getIntervalData(val) {
  if (!val || Object.keys(val).length === 0) return '';
  const lists = {days: '天', hours: '小时', seconds: '秒', minutes: '分钟'};
  return `每${val.every !== 1 ? val.every : ''}${lists[val.period]}`;
}
