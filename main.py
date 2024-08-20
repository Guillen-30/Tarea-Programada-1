import pandas as pd
from sqlalchemy import create_engine, text
from flask import Flask, jsonify, request
from flask_cors import CORS

def conexion_sql_server():
    connection_string = 'mssql+pyodbc://sa:BasesTec@25.8.143.41/Tarea Programada 1?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    engine = create_engine(connection_string)
    return engine

def select_to_df(params=None):
    try:
        sql_query = "EXEC SeleccionarEmpleados"
        engine = conexion_sql_server()
        df = pd.read_sql(sql_query, engine, params=params)
        if df is not None:
            df_sorted = df.sort_values(by='Nombre', ascending=True)
            print(df.to_json())
            print(type(df.to_dict(orient='records')))
        else:
            print("No se pudo obtener el DataFrame.")
    except Exception as e:
        print(f"ERROR: {e}")
    return df

def insert_to_db(name, salary):
    is_valid, message = validate_employee_data(name, salary)
    if not is_valid:
        return jsonify({"status": "error", "message": message})
    
    try:
        sql_query = text(f"EXEC InsertarEmpleado @Nombre='{name}', @Salario={salary}")
        engine = conexion_sql_server()
        with engine.connect() as connection :
            connection.execute(sql_query)
            connection.commit()

        #engine.execute(sql_query)
        return jsonify({"status": "success", "message": "Empleado insertado correctamente."})
    except Exception as e:
        print(f"\n\n\n{e}\n\n\n")
        return jsonify({"status": "error", "message": f"Error al insertar el empleado: {e}"})

def validate_employee_data(name, salary):
    if not isinstance(name, str) or len(name) < 3 or any(char.isdigit() for char in name):
        return False, "El nombre debe ser un string de al menos 3 caracteres y no debe contener números."
    
    try:
        salary = float(salary)
        if salary <= 0:
            return False, "El salario debe ser un número positivo."
    except ValueError:
        return False, "El salario debe ser un número válido."
    
    return True, "Datos válidos"


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/post-data', methods=['GET'])
def post_data():
    # Convert the DataFrame to a dictionary so it can be easily serialized to JSON
    df = select_to_df()
    df_sorted = df.sort_values(by='Nombre', ascending=True)
    data = df_sorted.to_dict(orient='records')
    print(f"Received data: {data}")
    
    # Return a response
    return jsonify({"status": "success", "data_received": data})

@app.route('/insert-employee', methods=['POST'])
def insert_employee():
    # Get the data from the JSON request body
    data = request.get_json()
    name = data.get('name')
    salary = data.get('salary')
    
    print(f"Received data: {name}, {salary}")
    response = insert_to_db(name, salary)

    return response
    

if __name__ == '__main__':
    app.run(debug=True)
