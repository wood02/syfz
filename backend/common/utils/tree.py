# -*- coding: utf-8 -*-

def xTree(data, parent_id=0):
    """
    查询指定 顶级父节点
    :param data:
    :param parent_id:
    :return:
    """
    tree_list = []
    tree_dict = {}
    for item in data:
        tree_dict[item['id']] = item
    for i in tree_dict:
        if tree_dict[i]['parent_id'] != parent_id:
            # 判断是否是顶级 不是顶级 获得父级
            p_id = tree_dict[i]['parent_id']

            # 如果是顶级节点并且指定节点不为顶级节点
            if p_id == 0 and parent_id != 0:
                continue
            tree = tree_dict[p_id]
            tree.setdefault('children', []).append(tree_dict[i])  # 将数据添加到父级树中
            # 如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。
        else:
            # 是顶级就直接加
            tree_dict[i]['children'] = []
            tree_list.append(tree_dict[i])
    return tree_list
