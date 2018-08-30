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
            if result is not None:
                return result
            return False

        except Exception as e:
            return "Error: " + str(e)

    def getUserByEmail(self,email):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM users WHERE email=%s"
            cursor.execute(sql,(email))
            result = cursor.fetchone()
            if result is not None:
                return result
            return False

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

    def getUserPassword(self,email):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM users WHERE email=%s"
            cursor.execute(sql,(email))
            result = cursor.fetchone()
            if result is not None:
                return result['password']
            return False

        except Exception as e:
            return "Error: " + str(e)

    def getAdminPassword(self,email):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM admin WHERE email=%s"
            cursor.execute(sql,(email))
            result = cursor.fetchone()
            if result is not None:
                return result['password']
            return False

        except Exception as e:
            return "Error: " + str(e)

    def getPendingUsers(self):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM users WHERE pending=1 AND trash=0"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()

            return result

        except Exception as e:
            return "Error: " + str(e)




    def getActiveUsers(self):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT users.id,users.season_id, users.fname,users.lname,users.tp,users.email,users.password,users.pending,users.trash, " \
                  "season.location_from, season.location_to,season.start_date,season.end_date,season.amount,season.date_payment,season.class,season.active " \
                  "FROM users LEFT JOIN season on users.season_id = season.id where users.pending = 0"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()

            return result

        except Exception as e:
            return "Error: " + str(e)

    def getSeasonByUserInactive(self,id):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM season WHERE active=0 and user_id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchall()
            conn.close()

            return result

        except Exception as e:
            return "Error: " + str(e)

    def getSeasonByUserActive(self,id):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM season WHERE active=1 and user_id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchone()
            conn.close()

            return result

        except Exception as e:
            return "Error: " + str(e)

    def getSeasonById(self,id):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM season WHERE id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchone()
            conn.close()

            return result

        except Exception as e:
            return "Error: " + str(e)

    def addSeason(self,user_id, location_from,location_to, season_class,active):
        try:
            conn, cursor = self.connection()
            sql = "INSERT INTO season (user_id,location_from,location_to,class,active) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql,(user_id,location_from,location_to,season_class,active))
            season_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return season_id

        except Exception as e:
            print("Error: ", str(e))

            return False

    def seasonCancel(self,season_id):
        try:
            conn, cursor = self.connection()
            sql = "UPDATE season SET active=0 WHERE id=%s"
            result = cursor.execute(sql,(season_id))
            conn.commit()
            conn.close()

            return result

        except Exception as e:
            print("Error: ", str(e))

            return False


    def setSeasonAmount(self,season_id,amount):
        try:
            conn, cursor = self.connection()
            sql = "UPDATE season SET amount=%s WHERE id=%s"
            result = cursor.execute(sql,(amount,season_id))
            conn.commit()
            conn.close()

            return result

        except Exception as e:
            print("Error: ", str(e))

            return False

    def setSeasonPayementDate(self,id,start_date,end_date,date_payment):
        try:
            conn, cursor = self.connection()
            sql = "UPDATE season SET start_date=%s , end_date=%s, date_payment=%s WHERE id=%s"
            result = cursor.execute(sql,(start_date,end_date,date_payment,id))
            conn.commit()
            conn.close()

            return result

        except Exception as e:
            print("Error: ", str(e))

            return False

    def updateUserSeasonId(self,user_id,season_id):
        try:
            conn, cursor = self.connection()
            sql = "UPDATE users SET season_id=%s WHERE id=%s"
            result = cursor.execute(sql,(season_id,user_id))
            conn.commit()
            conn.close()

            return result

        except Exception as e:
            print("Error: ", str(e))

            return False



    def approveUser(self,id):
        try:
            conn,cursor = self.connection()
            sql = "UPDATE users SET pending=0 WHERE id=%s AND trash=0"
            result = cursor.execute(sql,(id))
            conn.commit()
            conn.close()
            return result

        except Exception as e:
            return "Error: " + str(e)

    def trashUser(self,id):
        try:
            conn,cursor = self.connection()
            sql = "UPDATE users SET trash=1 WHERE id=%s"
            result = cursor.execute(sql,(id))
            conn.commit()
            conn.close()
            return result

        except Exception as e:
            return "Error: " + str(e)


    def getLocationList(self):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM locations"
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()
            return result

        except Exception as e:
            return "Error: " + str(e)


    def getAdminById(self,id):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM admin WHERE id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchone()
            conn.close()
            return result

        except Exception as e:
            return "Error: " + str(e)

    def getAdminByEmail(self,email):
        try:
            conn,cursor = self.connection()
            cursor = conn.cursor(DictCursor)
            sql = "SELECT * FROM admin WHERE email=%s"
            cursor.execute(sql,(email))
            result = cursor.fetchone()
            conn.close()
            return result

        except Exception as e:
            return "Error: " + str(e)







if __name__ == '__main__':
    db = Database()
    # print(db.regNewUser('fwef','fwef','0750998544','afaaa@gmail.com','pss'))
    # print(db.getUserById(14))
    # print(db.getUserPassword('e@gmail.com'))
    print(db.getSeasonByUserInactive(2))