import pymysql

def obtener_conexion():
    return pymysql.connect(host='dawa2024iiusat.mysql.pythonanywhere-services.com',
                                user='dawa2024iiusat',
                                password='abcDEF$123',
                                db='dawa2024iiusat$discos')