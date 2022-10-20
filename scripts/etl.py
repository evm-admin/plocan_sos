#!/usr/bin/env python
# coding: utf-8

# ## ETL del Proyecto:
# 'ESTUDIO Y SOPORTE TÉCNICO PARA LA IMPLEMENTACIÓN
# DEL ESTÁNDAR SWE EN PLATAFORMA DE SENSORES
# GESTIONADOS POR PLOCAN'
#
# Se tienen dos ficheros 'MERGED_ctd.csv' y 'MERGED_WEATHER.csv' que se van a limpiar y preparar para el script 'xml_creation_result.py'. Esta limpieza va a consistir en eliminar las columnas que no hagan falta para el proyecto, transformar las medidas en las unidades que se desee y crear un tercer fichero de salida que se corresponda con las variables medida por el DO.

import pandas as pd

# Ficheros de salida
ctd_output_name = "./csv_cleaned/ctd_cleaned.csv"
do_output_name = "./csv_cleaned/do_cleaned.csv"
weather_output_name = "./csv_cleaned/weather_cleaned.csv"
wg_output_name = "./csv_cleaned/wg_cleaned.csv"

ctd = pd.read_csv("MERGED_ctd.csv")
weather = pd.read_csv("MERGED_WEATHER.csv")
telemetry = pd.read_csv("MERGED_TELEMETRY.csv")

# Modificaciones generales a los csv
def clean_csv(df):
    """
    input:
        df: dataframe a limpiar
    output:
        df: dataframe limpio
    """
    # Eliminación de columnas innecesarias
    # df = df.drop(columns = ['Unnamed: 10', 'Unnamed: 11', 'Vehicle'])

    # Conversión de formatos
    df["TimeStamp"] = pd.to_datetime(df["TimeStamp"], infer_datetime_format=True)

    # Eliminamos duplicados de fecha, si existen
    df = df.drop_duplicates("TimeStamp")

    # Ordenamos en orden descendiente de fecha
    df = df.sort_values(by="TimeStamp", ascending=False)

    return df


ctd = clean_csv(ctd)
weather = clean_csv(weather)
telemetry = clean_csv(telemetry)


# ### Generación de csv CTD
ctd_output = ctd[
    [
        "TimeStamp",
        "Pressure",
        "Temperature",
        "Conductivity",
        "Latitude(deg)",
        "Longitude(deg)",
    ]
]


# ### Generación de csv DO
do_output = ctd[
    ["TimeStamp", "Oxygen", "Salinity (PSU)", "Latitude(deg)", "Longitude(deg)"]
]

# Simulación del cálculo del oxígeno disuelto (no es real)
do_output["DO"] = (
    ctd["Temperature"] * ctd["Pressure"]
    + do_output["Oxygen"] / do_output["Salinity (PSU)"]
)
do_output = do_output[
    ["TimeStamp", "Oxygen", "Salinity (PSU)", "DO", "Latitude(deg)", "Longitude(deg)"]
]


# ### Generación de csv weather
weather_output = weather[
    [
        "TimeStamp",
        "Temperature(degC)",
        "Wind Speed(kt)",
        "Wind Gust Speed(kt)",
        "Wind Direction",
        "Pressure(mb)",
        "Latitude",
        "Longitude",
    ]
]

# ### Generación WG
wg_output = telemetry[
    ["TimeStamp", "Distance Over Ground(m)", "Lat (deg)", "Lon (deg)"]
]

# ### Guardado de csv
ctd_output.to_csv(ctd_output_name, index=False)
do_output.to_csv(do_output_name, index=False)
weather_output.to_csv(weather_output_name, index=False)
wg_output.to_csv(wg_output_name, index=False)
