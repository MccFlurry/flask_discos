import pymysql

def obtener_conexion():
    return pymysql.connect(host='RogerZavM.mysql.pythonanywhere-services.com',
                                user='RogerZavM',
                                password='mrmilk12',
                                db='RogerZavM$discos')