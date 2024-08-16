import pandas as pd
from sqlalchemy import create_engine

def conexion_sql_server():
    connection_string = 'mssql+pyodbc://sa:BasesTec@25.8.143.41/Tarea Programada 1?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    engine = create_engine(connection_string)
    return engine

def select_to_df(sql_query, engine):
    try:
        df = pd.read_sql(sql_query, engine)
    except Exception as e:
        print(f"ERROR: {e}")
    return df

sql_query = "SELECT * FROM [dbo].[Empleado]"
engine = conexion_sql_server()
df = select_to_df(sql_query, engine)
if df is not None:
    print("Conexión y consulta exitosa.")
    print("Primeras filas del DataFrame:")
    print(df.head(40))  # Muestra las primeras 5 filas del DataFrame
    print("\nResumen del DataFrame:")
    print(df.info())  # Muestra un resumen de las columnas y el tipo de datos
else:
    print("No se pudo obtener el DataFrame.")
