from configs import *

# Función para obtener la conexión
def get_connection():
	return psycopg2.connect(
		host=pg_conn_data["host"],
		database=pg_conn_data["db"],
		user=pg_conn_data["user"],
		password=pg_conn_data["password"],
		port=pg_conn_data["port"]
	)

# Función para seleccionar datos de la tabla
def selectTable(table, columns="*", where=None, order=None, limit=None, offset=None):
	try:
		with get_connection() as conn:
			with conn.cursor() as cursor:

				# Construye la consulta SQL
				query = f"SELECT {columns} FROM {table}"
				params = []
				if where:
					query += f" WHERE {where}"
				if order:
					query += f" ORDER BY {order[0]} {order[1]}"
				if limit is not None:
					query += " LIMIT %s"
					params.append(limit)
				if offset is not None:
					query += " OFFSET %s"
					params.append(offset)

				cursor.execute(query, params)
				rows = cursor.fetchall()

				return [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]

	except psycopg2.Error as e:
		return {"error": f"Error de base de datos: {str(e)}"}

# Función para insertar datos en la tabla
def insertTable(table, data):
	try:
		with get_connection() as conn:
			with conn.cursor() as cursor:

				# Construir la consulta SQL de inserción
				columns = ', '.join(data.keys())
				placeholders = ', '.join(['%s' for _ in data])
				sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
				
				# Ejecutar la consulta SQL con los valores a insertar
				cursor.execute(sql, list(data.values()))
                
				# Obtener el ID del registro insertado
				inserted_id = cursor.fetchone()[0]

				# Confirmar la transacción
				conn.commit()

				return inserted_id

	except psycopg2.Error as e:
		return {"error": f"Error de base de datos: {str(e)}"}

# Función para actualizar datos en la tabla
def updateTable(table, data, where):
	try:
		with get_connection() as conn:
			with conn.cursor() as cursor:
				set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
				sql = f"UPDATE {table} SET {set_clause} WHERE {where}"

				cursor.execute(sql, list(data.values()))
				conn.commit()

				return "Actualización exitosa"

	except Exception as e:
		return {"error": f"Error de base de datos: {str(e)}"}

# Función para eliminar datos de la tabla
def deleteTable(table, where):
	try:
		with get_connection() as conn:
			with conn.cursor() as cursor:
				sql = f"DELETE FROM {table} WHERE {where}"
				cursor.execute(sql)
				conn.commit()

				return "Eliminación exitosa"

	except Exception as e:
		return {"error": f"Error de base de datos: {str(e)}"}

# Ejecuta consultas que devuelven resultados (SELECT)
def executeSQL(SQL):
	try:
		with get_connection() as conn:
			with conn.cursor() as cursor:
				cursor.execute(SQL)
				rows = cursor.fetchall()
				
				# Convertir resultados en lista de diccionarios
				return [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows] if rows else []

	except Exception as e:
		return {"error": f"Error de base de datos: {str(e)}"}

# Ejecuta consultas que no devuelven resultados (INSERT, UPDATE, DELETE)
def executeNonQuery(SQL):
	try:
		with get_connection() as conn:
			with conn.cursor() as cursor:
				cursor.execute(SQL)
				conn.commit()
				return "ok"

	except Exception as e:
		return {"error": f"Error de base de datos: {str(e)}"}