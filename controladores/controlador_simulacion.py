from bd import obtener_conexion

def insertar_simulacion(data, tasaimensual, cantidadmeses):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO simulacion(fechasimulacion, total, itotal, tasaimensual, cantidadmeses) VALUES (%s, %s, %s, %s, %s)",
                       (data["fechasimulacion"], data["total"], data["itotal"], tasaimensual, cantidadmeses))
        idsimulacion = conexion.insert_id()
        for cuota in data["cuotas"]:
            cursor.execute("INSERT INTO detallesimulacion(idsimulacion, mes, capital, interes, total) VALUES (%s, %s, %s, %s, %s)",
                       (idsimulacion, cuota["mes"], cuota["capital"], cuota["interes"], cuota["total"]))
    conexion.commit()
    conexion.close()
    return idsimulacion