/*
 * @Author: H0nGzA1
 * @Date: 2022-05-16 15:47:21
 * @LastEditors: hongzai 2505811377@qq.com
 * @LastEditTime: 2022-05-16 16:50:33
 * @FilePath: /web/src/views/system/dept/api.js
 * @Description:
 * email:2505811377@qq.com
 */
/*
 * @创建文件时间: 2021-06-01 22:41:21
 * @Auther: 猿小天
 * @最后修改人: 猿小天
 * @最后修改时间: 2021-09-26 21:17:30
 * 联系Qq:1638245306
 * @文件介绍: 部门管理接口
 */
import { request } from "@/api/service";
import XEUtils from "xe-utils";
export const urlPrefix = "/api/system/dept/";

/**
 * 列表查询
 */
export function GetList(query) {
  // query.limit = 999;
  return request({
    url: urlPrefix,
    method: "get",
    params: query,
  }).then((res) => {
    // 将列表数据转换为树形数据
    res.data.data = XEUtils.toArrayTree(res.data.data, {
      parentKey: "parent",
      strict: false,
    });
    return res;
  });
}
/**
 * 新增
 */
export function createObj(obj) {
  return request({
    url: urlPrefix,
    method: "post",
    data: obj,
  });
}

/**
 * 修改
 */
export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + "/",
    method: "put",
    data: obj,
  });
}
/**
 * 删除
 */
export function DelObj(id) {
  return request({
    url: urlPrefix + id + "/",
    method: "delete",
    data: { id },
  });
}

export function GetTreeChildrenByParentId(parentId) {
  return TreeNodesLazyLoader.getChildren(parentId);
}

export function GetNodesByValues(values) {
  return TreeNodesLazyLoader.getNodesByValues(values);
}

const getPcasData = request({
  url: "/api/system/dept_query/",
  method: "get",
}).then((res) => {
  // 将列表数据转换为树形数据
  res.data.data = XEUtils.toArrayTree(res.data.data, {
    parentKey: "parent",
    strict: false,
  });
  return res.data.data;
});
export default getPcasData;
export const TreeNodesLazyLoader = {
  getNodesByValues(values) {
    // console.log("getNodesByValues", values);
    if (!(values instanceof Array)) {
      values = [values];
    }
    return getPcasData.then((data) => {
      const nodes = [];
      for (const value of values) {
        const found = this.getNode(data, value);
        if (found) {
          nodes.push(found);
        }
      }
      return nodes;
    });
  },
  getNode(list, value) {
    for (const item of list) {
      if (item.code === value) {
        return item;
      }
      if (item.children && item.children.length > 0) {
        const found = this.getNode(item.children, value);
        if (found) {
          return found;
        }
      }
    }
  },
  getChildren(parent) {
    return getPcasData.then((data) => {
      const list = this.getChildrenByParent(parent, data);
      if (list == null) {
        return [];
      }
      return this.cloneAndDeleteChildren(list);
    });
  },
  getChildrenByParent(parentId, tree) {
    if (!parentId) {
      // 取第一级
      return tree;
    } else {
      for (const node of tree) {
        if (node.code === parentId) {
          return node.children;
        }
        if (node.children && node.children.length > 0) {
          // 递归查找
          const list = this.getChildrenByParent(parentId, node.children);
          if (list) {
            return list;
          }
        }
      }
    }
  },
  cloneAndDeleteChildren(list) {
    const newList = [];
    for (const node of list) {
      const newNode = {};
      Object.assign(newNode, node);
      if (newNode.children == null || newNode.children.length === 0) {
        newNode.isLeaf = true;
        newNode.leaf = true;
      }
      delete newNode.children;
      newList.push(newNode);
    }
    // console.log("found children:", newList);
    return newList;
  },
};
