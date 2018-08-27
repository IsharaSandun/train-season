import pymysql
from pymysql import escape_string as thwart
from pymysql.cursors import DictCursor,SSCursor,SSDictCursor


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

    def getUserById(self,id):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM users WHERE id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchone()
            return result

        except Exception as e:
            return "Error: " + str(e)

    def checkUserExists(self,email):
        try:
            conn, cursor = self.connection()
            sql = "SELECT * FROM users where email=%s"
            cursor.execute(sql,(email))
            result = len(cursor.fetchall())
            conn.close()

            if (result > 0):
                return True
            else:
                return False

        except Exception as e:
            return "Error: " + str(e)

    def regNewUser(self,fname,lname,tp,email,password):
        try:
            conn, cursor = self.connection()
            sql = "INSERT INTO users (fname,lname,tp,email,password) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql,(fname,lname,tp,email,password))
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return user_id

        except Exception as e:
            print("Error: ", str(e))

            return False


if __name__ == '__main__':
    db = Database()
    # print(db.regNewUser('fwef','fwef','0750998544','afaaa@gmail.com','pss'))
    print(db.getUserById(14))