import pymysql
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

def create_database_tables():

    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass)

    try:
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS soyHenryGrupal')
        conn.select_db('soyHenryGrupal')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders(
                id INT AUTO_INCREMENT PRIMARY KEY, 
                order_id VARCHAR (50) NOT NULL, 
                order_item_id int  NOT NULL, 
                customer_id VARCHAR(50)  NOT NULL,
                customer_unique_id VARCHAR(50)  NULL,
                customer_zip_code_prefix int   NULL,
                customer_city VARCHAR(50)   NULL, 
                customer_state VARCHAR(30)   NULL, 
                seller_id VARCHAR(50)  NOT NULL,
                seller_city VARCHAR(50)   NULL,
                seller_zip_code_prefix int,
                seller_state VARCHAR(30)   NULL, 
                review_id VARCHAR(50)  NULL, 
                product_id VARCHAR(50)  NOT NULL, 
                product_category_name VARCHAR(50)  NULL, 
                order_delivery_date DATE NULL,
                order_status VARCHAR(30)  NOT NULL,
                price DECIMAL(10,2), 
                freight_value DECIMAL(10,2), 
                review_score DECIMAL(10,2), 
                review_creation_date DATE NULL
            )
        ''')
        

        print("Se creó la tabla correctamente.")

    except Exception as e:
        print("No se pudo crear la base de datos y la tabla:", str(e))

    cursor.close()
    conn.close()

def insert_data_to_db(dforders):

    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass)
    cursor = conn.cursor()

    try:
        conn.select_db('soyHenryGrupal')
        # Iterar sobre los valores recibidos
        for index, row in dforders.iterrows():
            value_set = tuple(row)  # Convertir la fila a una tupla
            # Armar la sentencia SQL de inserción
            sql = '''
                INSERT INTO orders (
                    order_id, order_item_id, customer_id, customer_unique_id, customer_zip_code_prefix,
                    customer_city, customer_state, seller_id, seller_city, seller_zip_code_prefix,
                    seller_state, review_id, product_id, product_category_name, order_delivery_date,
                    order_status, price, freight_value, review_score, review_creation_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            '''
            print("se insertaron")
            # Ejecutar la sentencia SQL de inserción para cada conjunto de valores
            cursor.execute(sql, value_set)
            print("el codigo continua")
        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        cursor.close()
        conn.close()

        print("Datos insertados correctamente en la base de datos.")
    except Exception as e:
        print("Error al insertar datos:", str(e))