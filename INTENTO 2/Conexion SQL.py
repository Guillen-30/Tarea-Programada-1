import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify, request
from flask_cors import CORS

def conexion_sql_server():
    connection_string = 'mssql+pyodbc://sa:BasesTec@25.8.143.41/Tarea Programada 1?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes'
    engine = create_engine(connection_string)
    return engine

def select_to_df(sql_query, engine, params=None):
    try:
        df = pd.read_sql(sql_query, engine, params=params)
        return df
    except Exception as e:
        print(f"ERROR: {e}")
        return None

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

@app.route('/get-employees', methods=['GET'])
def get_employees():
    sql_query = "EXEC SeleccionarEmpleados"
    engine = conexion_sql_server()
    df = select_to_df(sql_query, engine)
    if df is not None:
        df_sorted = df.sort_values(by='Nombre', ascending=True)
        data = df_sorted.to_dict(orient='records')
        return jsonify({"status": "success", "data": data})
    else:
        return jsonify({"status": "error", "message": "No se pudo obtener el DataFrame."})

@app.route('/insert-employee', methods=['POST'])
def insert_employee():
    name = request.form['name']
    salary = request.form['salary']
    
    is_valid, message = validate_employee_data(name, salary)
    if not is_valid:
        return jsonify({"status": "error", "message": message})
    
    engine = conexion_sql_server()
    try:
        sql_query = f"EXEC InsertarEmpleado @Nombre='{name}', @Salario={salary}"
        engine.execute(sql_query)
        return jsonify({"status": "success", "message": "Empleado insertado correctamente"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al insertar empleado: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
    