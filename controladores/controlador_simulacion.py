from bd import obtener_conexion

def insertar_simulacion(data):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Simulacion (fecha_simulacion, capital, tasa_mensual, cantidad_meses) "
            "VALUES (%s, %s, %s, %s)",
            (data["fecha_simulacion"], data["capital"], data["tasa_mensual"], data["cantidad_meses"])
        )
        id_simulacion = cursor.lastrowid

        for cuota in data["cuotas"]:
            cursor.execute(
                "INSERT INTO DetallesCuotas (id_simulacion, mes, capital, interes, total_cuota) "
                "VALUES (%s, %s, %s, %s, %s)",
                (id_simulacion, cuota["mes"], cuota["capital"], cuota["interes"], cuota["total"])
            )

    conexion.commit()
    conexion.close()
    return id_simulacion