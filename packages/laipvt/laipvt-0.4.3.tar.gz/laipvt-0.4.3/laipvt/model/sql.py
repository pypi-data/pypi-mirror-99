from __future__ import absolute_import
from __future__ import unicode_literals
import re
import pymysql
from laipvt.helper.exception import ModelError


class SqlModule(object):
    def __init__(self, *args, **kwargs):
        self.conn = pymysql.connect(**kwargs)

    def use_db(self, db_name):
        self.conn.select_db(db_name)

    def _read_file(self, file_path, eof=';'):
        try:
            with open(file_path) as f:
                ret = f.read()
                ret = re.sub(r'/\*.*?\*/', "\n", ret, flags=re.S)
                ret = re.sub(r"--.*\n", "\n", ret)
                ok = ret.split(eof)
                return ok
        except Exception as e:
            raise ModelError("SqlModule._read_file, 读取文件失败，文件路径: {}, 错误信息: {}".format(file_path, e)) from None

    def _read_file_lines(self, file_path, eof=";"):
        try:
            with open(file_path) as f:
                content = f.readlines()
                result = []
                sql = ""
                for line in content:
                    if not line.strip():
                        continue
                    sql += line.strip()
                    if line.strip().find(eof) >= 0:
                        ret = re.sub(r'/\*.*?\*/', "\n", sql, flags=re.S)
                        ret = re.sub(r"--.*\n", "\n", ret)
                        result.append(ret)
                        sql = ""
                return result
        except Exception as e:
            raise ModelError("SqlModule._read_file, 读取文件失败，文件路径: {}, 错误信息: {}".format(file_path, e)) from None

    def import_from_file(self, path, file_eof=";"):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        for sql_request in self._read_file(path, file_eof):
            if sql_request.strip():
                try:
                    cursor.execute(sql_request)
                except Exception as e:
                    try:
                        new_sql = sql_request.split(file_eof)
                        for s in new_sql:
                            if len(s) > 0:
                                try:
                                    cursor.execute(s)
                                except Exception as e:
                                    raise e
                    except Exception as e:
                        raise ModelError("SqlModule.import_from_file, 错误信息: {}".format(e)) from None
        cursor.close()

    def import_from_file_commander(self, path, file_eof=";"):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        for sql_request in self._read_file_lines(path, file_eof):
            if sql_request.strip():
                try:
                    cursor.execute(sql_request)
                except Exception as e:
                    try:
                        new_sql = sql_request.split(file_eof)
                        for s in new_sql:
                            if len(s) > 0:
                                try:
                                    cursor.execute(s)
                                except Exception as e:
                                    raise e
                    except Exception as e:
                        raise ModelError("SqlModule.import_from_file, 错误信息: {}".format(e)) from None
        cursor.close()


    def insert_sql(self, sql_statements):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_statements)
            self.conn.commit()
        except Exception as e:
            raise ModelError("SqlModule.insert_sql, 错误信息: {}".format(e)) from None
        finally:
            cursor.close()


    def select(self, sql_statements):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql_statements)
            info = cursor.fetchall()
        except Exception as e:
            raise ModelError("SqlModule.select, 错误信息: {}".format(e)) from None
        finally:
            cursor.close()
            return True if info is not None else False

    def run_sql(self, sql):
        cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            cursor.execute(sql)
        except Exception as e:
            raise ModelError("SqlModule.run_sql, 错误信息: {}".format(e)) from None
        finally:
            cursor.close()

    def close(self):
        self.conn.close()