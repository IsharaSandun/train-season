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
            conn.close()
            return "Database Connection Success"
        except Exception as e:
            return "Error: " + str(e)

    def getNextUserId(self):
        try:
            conn,cursor = self.connection()
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            count = len(cursor.fetchall())
            return count

        except Exception as e:
            return "Error: " + str(e)

    def checkUserExists(self,email):
        try:
            conn, cursor = self.connection()
            sql = "SELECT * FROM users where email=%s"
            cursor.execute(sql,(email))
            result = len(cursor.fetchone())
            conn.close()

            if (result > 0):
                return True
            else:
                return False

        except Exception as e:
            return "Error: " + str(e)



    def regNewUser(self,fname,lname,email,password):
        try:
            conn, cursor = self.connection()
            sql = "INSERT INTO users (fname,lname,email,password) VALUES (%s,%s,%s,%s)"
            result = cursor.execute(sql,(fname,lname,email,password))
            conn.commit()
            conn.close()
            return result
        except Exception as e:
            return "Error: " + str(e)


db = Database()
# print(db.checkDb())
# print(db.userCount())
print(db.regNewUser('Ishara','Sandun','ishara@gmail.com','pss'))
# print(db.checkUserExists('ishara@gmail.com'))