"""
Describe:数据库工具初始化
Author:nekorose
CreateDate:20220911
"""
from dbTools.sqlite3orm import Sqlite3Connection
from content.setting import Sqlite_db

Sqlite3Connection.set_db(Sqlite_db)
