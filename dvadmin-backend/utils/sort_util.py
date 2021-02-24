"""
封装排序:
  ● 普通类型列表的排序
  ● 字典列表的排序
  ● 对象列表的排序
"""
import operator
from collections import Iterable


def sortSimpleTypeList(li, reverse=False):
    """
    排序简单的类型
    :param li:
    :param reverse:
    :return:
    """
    li.sort()
    if reverse:
        li.reverse()
    return li


def sortObjectList(obj_list, by_prop):
    """
    排序列表:按照对象的某个属性排序
    :param obj_list:
    :param by_prop:
    :return:
    """
    reverse = False
    if by_prop.startswith('-'):
        reverse = True
        by_prop = by_prop[1:]
    fun = operator.attrgetter(by_prop)
    obj_list.sort(key=fun)
    if reverse:
        obj_list.reverse()
    return obj_list


def sortDictList(dict_list, by_key):
    """
    排序字典列表:按照字典的某个key的value排序
    :param dict_list:
    :param by_key:
    :return:
    """
    reverse = False
    if by_key.startswith('-'):
        reverse = True
        by_key = by_key[1:]
    dict_list.sort(key=lambda ele: ele[by_key])
    if reverse:
        dict_list.reverse()
    return dict_list


def sortList(li, by=''):
    """
    排序集合: by加上前缀'-'表示逆序
    :param li: 字典集合 or 对象集合
    :param by: 通过哪一个属性, name 按照name排序; -name 按照name反向排序
    :return: 原对象(排序后集合, 不是返回新集合)
    """
    reverse = False
    if not li or not isinstance(li, Iterable):
        # 不是集合, 或空集合返回原内容
        return li
    if by.startswith('-'):
        reverse = True
    if isinstance(li[0], (int, float, str)):
        return sortSimpleTypeList(li, reverse)
    if not by:
        # 非简单类型的list, 必须要传入by, 否则不排序
        return li
    if isinstance(li[0], dict):
        # 如果第一个元素是字典类型,则默认所有元素都是字典类型
        return sortDictList(li, by)
    return sortObjectList(li, by)
