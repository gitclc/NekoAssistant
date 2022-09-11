"""
Describe:程序主入口
Author:nekorose
CreateDate:20220904
"""


# TODO 初始化
# TODO 功能
# TODO 命令处理
# TODO 数据存储

# TODO command版本
class CommandPage:
    def __init__(self):
        pass


if __name__ == '__main__':
    from content.setting import Sqlite_db
    from dbTools.sqlite3orm import ModelTest
    from datetime import datetime

    a = ModelTest()
    print(a.field_list)
    print(a.tb_name)
    # a.insert(create_data=datetime.now(), name='nekorose')
