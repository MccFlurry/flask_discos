from bd import obtener_conexion

def obtener_user_por_email(email):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        sql  = " SELECT id, email, password FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
    conexion.close()
    return user

def obtener_user_por_id(id):
    conexion = obtener_conexion()
    user = None
    with conexion.cursor() as cursor:
        sql  = " SELECT id, email, password FROM users WHERE id = %s"
        cursor.execute(sql, (id,))
        user = cursor.fetchone()
    conexion.close()
    return user

def registrar_usuario(email, password):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        sql  = " INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(sql, (email, password, ))
    conexion.commit()
    conexion.close()