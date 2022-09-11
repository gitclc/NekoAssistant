"""
Describe:数据库工具
Author:nekorose
CreateDate:20220904
"""
import sqlite3
import sys
import os
from datetime import datetime


# TODO sqlite3 连接类，连接池
class Sqlite3Connection:
    __sqlite_pool = {}
    __dbConfig = None

    @classmethod
    def connection(cls):
        """
        根据数据库的配置创建连接池
        数据库的配置使用set_db来设置
        :return:
        """
        if isinstance(cls.__dbConfig, dict):
            for db_name in cls.__dbConfig:
                db_path = cls.__dbConfig[db_name]
                cls.__sqlite_pool[db_name] = sqlite3.connect(db_path)
        else:
            raise Exception(f'请使用{cls.__class__.__name__}.{cls.set_db.__name__}配置数据库')

    @classmethod
    def set_db(cls, dbConfig):
        """
        :param dbConfig: 数据库配置，支持多个配置
        example:
        {
            'default': './database/NekoDb.db'
        }
        :return:
        """
        cls.__dbConfig = dbConfig

    @classmethod
    def get_con(cls, name):
        """
        获取连接，连接池不存在时会进行初始化
        :param name:
        :return:
        """
        if not cls.__sqlite_pool:
            cls.connection()
        return cls.__sqlite_pool[name]

    def __del__(self):
        for i in self.__sqlite_pool:
            try:
                self.__sqlite_pool[i].close()
            except:
                del self.__sqlite_pool[i]
                continue


# TODO ORM类
class FieldBase:
    __text = 'text'
    __field_type_map = {
        datetime: __text,
        str: __text,
    }

    def __init__(self, _type, null=True, default=None, **kwargs):
        """
        :param _type:字段类型，需要是python的一个类，判断和创建数据时会使用
        :param kwargs: 类创建对象时需要传入的参数
        """
        self.type = _type
        self.null = null
        self.default = default
        self.kwarg = kwargs

    def get_desc(self):
        _type = self.__field_type_map[self.type]
        require_list = [_type, 'null' if self.null else 'not null']
        if self.default:
            require_list.append('default %s' % self.default)
        return ' '.join(require_list)


class ModelBase:
    _db_name = 'default'
    _tb_name = None

    def __init__(self):
        self.tb_name = self._tb_name or self.__class__.__name__

        cls_dict = self.__class__.__dict__
        self.field_list = list(i for i in cls_dict.keys() if isinstance(cls_dict[i], FieldBase))
        self.con = Sqlite3Connection.get_con(self._db_name)
        self.cursor = self.con.cursor()
        self.__create_table()

    def insert(self, **kwargs):
        sql = '''
        '''
        print(sql)

    def __create_table(self):
        """
        创建表
        :return:
        """
        create_sql = "create table if not exists {0} ({1})"
        desc_list = list()
        for field in self.field_list:
            field_obj = getattr(self, field)
            field_desc = ' '.join([field, field_obj.get_desc()])
            desc_list.append(field_desc)
        desc_str = ','.join(desc_list)
        create_sql = create_sql.format(self._tb_name, desc_str)
        self.cursor.execute(create_sql)
        self.con.commit()


class ModelTest(ModelBase):
    _tb_name = 'test'
    create_data = FieldBase(_type=datetime, null=False)
    name = FieldBase(_type=str)


if __name__ == '__main__':
    pass
