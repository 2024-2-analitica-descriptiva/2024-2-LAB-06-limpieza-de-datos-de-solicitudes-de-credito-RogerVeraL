"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import glob
import os
import pandas as pd

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    def cargar_datos(directorio_entrada):
        for archivo in glob.glob(os.path.join(directorio_entrada, "*.csv")):
            return pd.read_csv(archivo, sep=";", index_col=0)

    def eliminar_duplicados_y_faltantes(df):
        df = df.drop_duplicates()
        df = df.dropna()
        return df

    def procesar_fechas(df):

        def convertir_fecha(fecha):
            if "/" in fecha:
                partes = fecha.split("/")
                if len(partes[0]) > 2:
                    return f"{partes[0]}-{partes[1]}-{partes[2]}"
                else: 
                    return f"{partes[2]}-{partes[1]}-{partes[0]}"
            return fecha 

        df["fecha_de_beneficio"] = df["fecha_de_beneficio"].map(convertir_fecha)
        df["fecha_de_beneficio"] = pd.to_datetime(df["fecha_de_beneficio"], errors="coerce")
        return df

    def limpiar_textos(df):
        columnas = df.columns.tolist()
        columnas.remove("barrio")

        df["barrio"] = df["barrio"].map(
            lambda x: x.lower().replace("_", "-").replace("-", " ")
        )

        df[columnas] = df[columnas].applymap(
            lambda x: (
                x.lower()
                .replace("-", " ")
                .replace("_", " ")
                .replace("$", "")
                .replace(".00", "")
                .replace(",", "")
                .strip()
                if isinstance(x, str)
                else x
            )
        )
        return df

    def guardar_archivo(df, directorio_salida, nombre_archivo):
        ruta_salida = os.path.join(directorio_salida, nombre_archivo)
        if os.path.exists(ruta_salida):
            os.remove(ruta_salida)
        os.makedirs(directorio_salida, exist_ok=True)
        df.to_csv(ruta_salida, sep=";", index=False)

    directorio_entrada = "files/input"
    directorio_salida = "files/output"
    nombre_archivo = "solicitudes_de_credito.csv"

    df = cargar_datos(directorio_entrada)
    df = eliminar_duplicados_y_faltantes(df)
    df = procesar_fechas(df)
    df = limpiar_textos(df)
    df = eliminar_duplicados_y_faltantes(df)  # Eliminar duplicados nuevamente tras limpiar
    guardar_archivo(df, directorio_salida, nombre_archivo)

pregunta_01()

