#!/usr/bin/env python
# encoding:utf-8

class Page(object):
    def __init__(self, model):
        self.model = model

    def to(self):
        return {
            "page": self.model.current_page,
            "page_count": self.model.per_page,
            "total_page": self.model.last_page,
            "total_count": self.model.total,
            "list": self.model.serialize()
        }


# 面向对象分页
class Pagination(object):

    def __init__(self, data_list, page, page_size=10):
        """
        初始化
        :param data_list: 所有数据列表
        :param page: 当前要查看的列表页
        :param page_size: 每页默认要显示几条
        """
        self.data_list = data_list
        self.page = page
        self.page_size = page_size

    @property
    def start(self):
        """
        计算引索的起始位置
        :return:
        """
        return (self.page - 1) * self.page_size

    @property
    def end(self):
        """
        计算引索的结束位置
        :return:
        """
        return self.page * self.page_size

    def show(self):
        """
        切片取数据,展示对应分页的结果
        :return:
        """
        data = {
            "page": self.page,
            "page_size": self.page_size,
            "count": len(self.data_list),
        }
        result = self.data_list[self.start:self.end]
        data["results"] = result

        return data


if __name__ == '__main__':

    data_list = []
    for i in range(1, 901):
        data_list.append('豆谷云-%s' % i)
    obj = Pagination(data_list, page=-1, page_size=10000)
    obj.show()
    print(obj.show())