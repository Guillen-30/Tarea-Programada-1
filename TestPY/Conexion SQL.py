import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify
from flask_cors import CORS


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
    print(df.to_json())
    print(type(df.to_dict(orient='records')))
else:
    print("No se pudo obtener el DataFrame.")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/post-data', methods=['POST',"GET"])
def post_data():
    # Convert the DataFrame to a dictionary so it can be easily serialized to JSON
    df = select_to_df(sql_query, engine)
    
    data = df.to_dict(orient='records')
    print(f"Received data: {data}")
    
    # Return a response
    return jsonify({"status": "success", "data_received": data})

if __name__ == '__main__':
    app.run(debug=True)
