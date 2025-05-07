from app.utils.excel_writer import procesar_txt_y_guardar_excel

import pandas as pd

# Función para procesar el archivo de pagos a proveedores
def procesar_archivo_service_proveedores(nombre_archivo: str):
    ruta_txt = f"uploads/{nombre_archivo}"
    columnas = ["Nro.", "Florícola", "Monto a pagar", "Periodo", "Acción"]
    
    # Lógica para procesar el archivo
    with open(ruta_txt, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    # Limpiar encabezados si es necesario
    encabezados = ["Nro.", "Florícola", "Monto a pagar", "Periodo", "Acción"]
    lineas = [linea for linea in lineas if linea.strip() not in encabezados]

    # Agrupar por bloques de 5 líneas
    filas = [lineas[i:i+5] for i in range(1, len(lineas), 5)]

    # Crear el dataframe
    df = pd.DataFrame(filas, columns=columnas)
    nombre_excel = nombre_archivo.replace(".txt", "_procesado.xlsx")
    
    # Guardar el archivo Excel
    df.to_excel(f"output/{nombre_excel}", index=False)

    return f"Archivo procesado: {nombre_excel}"

# Función para procesar el archivo de compras para coordinar
def procesar_archivo_service_compras(nombre_archivo: str):
    ruta_txt = f"uploads/{nombre_archivo}"
    columnas = ["Nro.", "Marcación", "País", "Fecha de Vuelo", "Fecha Creación", "FullBoxes", "Estado", "Revisado", "Revisado", "Acción"]
    
    # Lógica para procesar el archivo
    with open(ruta_txt, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    # Limpiar encabezados si es necesario
    encabezados = ["Nro.", "Marcación", "País", "Fecha de Vuelo", "Fecha Creación", "FullBoxes", "Estado", "Revisado", "Acción"]
    lineas = [linea for linea in lineas if linea.strip() not in encabezados]

    # Agrupar por bloques de 7-9 líneas
    filas = []
    i = 0
    while i + 6 < len(lineas):
        nro = lineas[i]
        marcacion = lineas[i + 1]
        pais = lineas[i + 2]
        vuelo = lineas[i + 3].replace("-", "/")
        creacion = lineas[i + 4].replace("-", "/")
        fullboxes = lineas[i + 5]
        estado = lineas[i + 6]

        revisado1, revisado2, accion = "", "", ""
        if i + 7 < len(lineas) and lineas[i + 7] in ("Comprar", "Ver compra"):
            revisado1 = lineas[i + 7]
            if i + 8 < len(lineas) and lineas[i + 8] == "Aprobar":
                revisado2 = lineas[i + 8]
                i += 9
            else:
                i += 8
        else:
            i += 7

        filas.append([nro, marcacion, pais, vuelo, creacion, fullboxes, estado, revisado1, revisado2, accion])

    # Crear el dataframe
    df = pd.DataFrame(filas, columns=columnas)
    nombre_excel = nombre_archivo.replace(".txt", "_procesado_compras.xlsx")

    # Guardar el archivo Excel
    df.to_excel(f"output/{nombre_excel}", index=False)

    return f"Archivo procesado: {nombre_excel}"
