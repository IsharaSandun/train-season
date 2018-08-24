import pymysql
from pymysql import escape_string as thwart


class Database:
    def __init__(self):
        return None

    def connection(self):
        conn = pymysql.connect(host='localhost',
                               user='root',
                               password='',
                               db='train_season')
        cursor = conn.cursor()

        return conn, cursor

    def checkDb(self):
        try:
            conn, cursor = self.connection()
            sql = "SELECT * FROM locations"
            x = cursor.execute(sql)
            result = cursor.fetchone()[1]
            return result
        except Exception as e:
            return "Error: " + str(e)
        finally:
            conn.close()

    def regNewUser(self):
        try:
            conn, cursor = self.connection()
            sql = "SELECT * FROM locations WHERE id=2"
            x = cursor.execute(sql)
            result = cursor.fetchone()[1]
            return result
        except Exception as e:
            return "Error: " + str(e)
        finally:
            conn.close()


# db = Database()
# print(db.checkDb())
# print(db.regNewUser())
