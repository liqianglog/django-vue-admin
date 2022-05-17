import { request } from '@/api/service'
import XEUtils from 'xe-utils'
export const urlPrefix = '/api/system/dept/'

/**
 * 列表查询
 */
export function GetList (query) {
  // query.limit = 999;
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  }).then((res) => {
    // 将列表数据转换为树形数据
    res.data.data = XEUtils.toArrayTree(res.data.data, {
      parentKey: 'parent',
      strict: false
    })
    return res
  })
}
/**
 * 新增
 */
export function createObj (obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 修改
 */
export function UpdateObj (obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}
/**
 * 删除
 */
export function DelObj (id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

export function GetTreeChildrenByParentId (parentId) {
  return TreeNodesLazyLoader.getChildren(parentId)
}

export function GetNodesByValues (values) {
  return TreeNodesLazyLoader.getNodesByValues(values)
}

const getPcasData = request({
  url: '/api/system/dept_query/',
  method: 'get'
}).then((res) => {
  // 将列表数据转换为树形数据
  res.data.data = XEUtils.toArrayTree(res.data.data, {
    parentKey: 'parent',
    strict: false
  })
  return res.data.data
})
export default getPcasData
export const TreeNodesLazyLoader = {
  getNodesByValues (values) {
    // console.log("getNodesByValues", values);
    if (!(values instanceof Array)) {
      values = [values]
    }
    return getPcasData.then((data) => {
      const nodes = []
      for (const value of values) {
        const found = this.getNode(data, value)
        if (found) {
          nodes.push(found)
        }
      }
      return nodes
    })
  },
  getNode (list, value) {
    for (const item of list) {
      if (item.code === value) {
        return item
      }
      if (item.children && item.children.length > 0) {
        const found = this.getNode(item.children, value)
        if (found) {
          return found
        }
      }
    }
  },
  getChildren (parent) {
    return getPcasData.then((data) => {
      const list = this.getChildrenByParent(parent, data)
      if (list == null) {
        return []
      }
      return this.cloneAndDeleteChildren(list)
    })
  },
  getChildrenByParent (parentId, tree) {
    if (!parentId) {
      // 取第一级
      return tree
    } else {
      for (const node of tree) {
        if (node.code === parentId) {
          return node.children
        }
        if (node.children && node.children.length > 0) {
          // 递归查找
          const list = this.getChildrenByParent(parentId, node.children)
          if (list) {
            return list
          }
        }
      }
    }
  },
  cloneAndDeleteChildren (list) {
    const newList = []
    for (const node of list) {
      const newNode = {}
      Object.assign(newNode, node)
      if (newNode.children == null || newNode.children.length === 0) {
        newNode.isLeaf = true
        newNode.leaf = true
      }
      delete newNode.children
      newList.push(newNode)
    }
    // console.log("found children:", newList);
    return newList
  }
}
