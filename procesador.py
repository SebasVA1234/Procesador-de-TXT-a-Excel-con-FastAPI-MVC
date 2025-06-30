import pandas as pd

def procesar_archivo(path_txt: str) -> str:
    nombre_archivo = path_txt.split("/")[-1]

    if "pagos" in nombre_archivo:
        return procesar_proveedores(path_txt, nombre_archivo)
    else:
        return procesar_compras(path_txt, nombre_archivo)

def procesar_proveedores(path_txt, nombre_archivo):
    columnas = ["Nro.", "Florícola", "Monto a pagar", "Periodo", "Acción"]

    with open(path_txt, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()

    encabezados = columnas
    lineas = [linea.strip() for linea in lineas if linea.strip() and linea.strip() not in encabezados]
    filas = [lineas[i:i+5] for i in range(1, len(lineas), 5)]
    df = pd.DataFrame(filas, columns=columnas)

    nombre_excel = f"output/{nombre_archivo.replace('.txt', '_procesado.xlsx')}"
    df.to_excel(nombre_excel, index=False)
    return nombre_excel

def procesar_compras(path_txt, nombre_archivo):
    columnas = ["Nro.", "Marcación", "País", "Fecha de Vuelo", "Fecha Creación", "FullBoxes", "Estado", "Revisado", "Revisado", "Acción"]

    with open(path_txt, 'r', encoding='utf-8') as archivo:
        lineas = [linea.strip() for linea in archivo if linea.strip()]

    encabezados = columnas
    lineas = [linea for linea in lineas if linea not in encabezados]

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

    df = pd.DataFrame(filas, columns=columnas)
    nombre_excel = f"output/{nombre_archivo.replace('.txt', '_procesado_compras.xlsx')}"
    df.to_excel(nombre_excel, index=False)
    return nombre_excel