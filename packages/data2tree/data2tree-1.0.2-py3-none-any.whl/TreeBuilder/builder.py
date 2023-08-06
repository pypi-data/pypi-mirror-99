# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Author:       01
# Date:         2021-03-22 13:25
# Description:  递归构建树

# -------------------------------------------------------------------------------

class BuildTree:
    def __init__(self, record_key: str, parent_record_key: str):
        self.record_key = record_key
        self.parent_record_key = parent_record_key

    # 构造Tree
    def build_tree(self, record_lst):
        final_tree = []
        for item in record_lst:
            if item[self.parent_record_key] == 0:  # 起始
                final_tree.append(item)
                self.build_leaf(item, record_lst)
        return final_tree

    # 创建此节点的孩子节点
    def build_leaf(self, node, record_lst):
        child_lst = self.get_child(node, record_lst)
        if child_lst:
            node["child"] = child_lst
            for item in child_lst:
                self.build_leaf(item, record_lst)

    # 获取此节点的孩子节点
    def get_child(self, node, record_lst):
        child_lst = []
        for item in record_lst:
            pid = item["pid"]
            if node[self.record_key] == pid:
                child_lst.append(item)
        return child_lst


# if __name__ == "__main__":
#     lst = [
#         {"id": 1, "pid": 0, "name": "Tree - 1"},
#         {"id": 2, "pid": 1, "name": "Tree - 1 - 1"},
#         {"id": 3, "pid": 1, "name": "Tree - 1 - 2"},
#         {"id": 4, "pid": 2, "name": "Tree - 1 - 1- 1"},
#         {"id": 5, "pid": 0, "name": "Tree - 2"}
#     ]
#
#     tree = BuildTree(record_key="id", parent_record_key="pid").build_tree(lst)
#     print(tree)