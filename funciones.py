''' En este archivo .py se definiran y desarrollaran funciones necesarias para realizar 
los procesos de ETL y EDA del proyecto'''

import pandas as pd
from textblob import TextBlob
import re

# Funciones
# Funcion tipo_de_datos: 
''''
Esta funcion realiza un análisis de los tipos de datos y la presencia de valores nulos 
en un DataFrame.

Para ello toma un DataFrame como entrada y devuelve un resumen que incluye información sobre
los tipos de datos en cada columna, el porcentaje de valores no nulos y nulos, así como la
cantidad de valores nulos por columna.
'''

def tipo_de_datos(df):
     mi_dict = {"nombre_campo": [], "tipo_datos": [], "no_nulos_%": [], "nulos_%": [], "nulos": []}
     for columna in df.columns:
        porcentaje_no_nulos = (df[columna].count() / len(df)) * 100
        mi_dict["nombre_campo"].append(columna)
        mi_dict["tipo_datos"].append(df[columna].apply(type).unique())
        mi_dict["no_nulos_%"].append(round(porcentaje_no_nulos, 2))
        mi_dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        mi_dict["nulos"].append(df[columna].isnull().sum())
     
     df_info = pd.DataFrame(mi_dict)
     
     return df_info

# Funcion duplicados:
''''
Verifica y muestra filas duplicadas en un DataFrame basado en una columna específica.

Esta función toma como entrada un DataFrame y el nombre de una columna específica.
Luego, identifica las filas duplicadas,las filtra y las ordena para una comparación 
más sencilla.
'''
def duplicados(df,columna):
    duplicated_rows = df[df.duplicated(subset=columna, keep=False)]
    if duplicated_rows.empty:
        return "No hay duplicados"
    
    # se ordenan las filas duplicadas para comparar entre sí
    duplicated_rows_sorted = duplicated_rows.sort_values(by=columna)
    return duplicated_rows_sorted

# Funcion sentiment_analisis:
'''
    Realiza un análisis de sentimiento en un texto dado y devuelve un valor numérico que representa el sentimiento.

    Esta función utiliza la librería TextBlob para analizar el sentimiento y
    asigna un valor numérico de acuerdo a la polaridad del sentimiento.
'''

def sentiment_analisis(review):
    if review is None:
        return 1
    analysis = TextBlob(review)
    polarity = analysis.sentiment.polarity
    if polarity < -0.2:
        return 0  
    elif polarity > 0.2: 
        return 2 
    else:
        return 1 
    
# Funcion ejemplos_review: 
    '''
    Imprime ejemplos de reviews para cada categoría de análisis de sentimiento.

    '''
def ejemplos_review(reviews, sentiments):
    for sentiment_value in range(3):
        print(f"Para la categoría de análisis de sentimiento {sentiment_value} se tienen estos ejemplos de reviews:")
        sentiment_reviews = [review for review, sentiment in zip(reviews, sentiments) if sentiment == sentiment_value]
        
        for i, review in enumerate(sentiment_reviews[:3], start=1):
            print(f"Review {i}: {review}")
        
        print("\n")


#Funcion extraer_año: 
'''
    Extrae el año de una fecha en formato 'yyyy-mm-dd' y maneja valores nulos.

    Esta función toma como entrada una fecha en formato 'yyyy-mm-dd' y devuelve el año de la fecha si
    el dato es válido. Si la fecha es nula o inconsistente, devuelve 'Dato no disponible'.
'''
def extraer_año(fecha):
    
    if pd.notna(fecha):
        if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
            return fecha.split('-')[0]
    return 'Dato no disponible'

# Funcion formato_fecha:
'''
    Convierte una cadena de fecha en un formato específico a otro formato de fecha.
'''
def formato_fecha(cadena_fecha):
    match = re.search(r'(\w+\s\d{1,2},\s\d{4})', cadena_fecha)
    if match:
        fecha_str = match.group(1)
        try:
            fecha_dt = pd.to_datetime(fecha_str)
            return fecha_dt.strftime('%Y-%m-%d')
        except:
            return 'Fecha inválida'
    else:
        return 'Formato inválido'

# Funcion convierte_float:
'''
    Reemplaza valores no numéricos y nulos en una columna con 0.0.

    Esta función toma un valor como entrada y trata de convertirlo a un número float.
    Si la conversión es exitosa, el valor numérico se mantiene. Si la conversión falla o
    el valor es nulo, se devuelve 0.0 en su lugar.
'''
def convierte_float(value):
    if pd.isna(value):
        return 0.0
    try:
        float_value = float(value)
        return float_value
    except:
        return 0.0

# Funcion porcentaje_bool: 
'''
    Cuanta la cantidad de True/False luego calcula el porcentaje.
''' 
def porcentaje_bool(df, columna):
    counts = df[columna].value_counts()
    percentages = round(100 * counts / len(df),2)
    # Crea un dataframe con el resumen
    df_results = pd.DataFrame({
        "Cantidad": counts,
        "Porcentaje": percentages
    })
    return df_results

# Funcion bigote_max:
'''
    Calcula el valor del bigote superior y la cantidad de valores atípicos en una columna.
'''
def bigote_max(columna):
    # Cuartiles
    q1 = columna.describe()[4]
    q3 = columna.describe()[6]

    # Valor del vigote
    bigote_max = round(q3 + 1.5*(q3 - q1), 2)
    print(f'El bigote superior de la variable {columna.name} se ubica en:', bigote_max)

    # Cantidad de atípicos
    print(f'Hay {(columna > bigote_max).sum()} valores atípicos en la variable {columna.name}')
