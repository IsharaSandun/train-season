import pymysql

def Connection():
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='train_season')
    c = conn.cursor()
    return c, conn