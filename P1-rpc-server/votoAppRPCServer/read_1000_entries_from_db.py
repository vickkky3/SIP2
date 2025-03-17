import psycopg2
import time
import statistics

# Configuración de conexión a PostgreSQL en VM1
#DB_CONFIG = {
#    'dbname': 'voto',
#    'user': 'alumnodb',
#    'password': 'tu_contraseña',
#    'host': '127.0.0.1',  # O la IP de VM1
#    'port': '15432'
#}

DB_CONFIG = {
    'dbname': 'voto',
    'user': 'alumnodb',
    'password': 'npg_luUM7s6YbnpH',
    'host': 'ep-wild-mountain-a8j6dy6y-pooler.eastus2.azure.neon.tech',  # O la IP de VM1
}
def medir_lectura():
    tiempos = []
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for _ in range(7):  # Ejecutamos 7 mediciones
            inicio = time.time()
            cursor.execute("SELECT * FROM voto LIMIT 1000")
            cursor.fetchall()  # Obtener todos los registros
            fin = time.time()
            tiempos.append(fin - inicio)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error en la conexión: {e}")
        return

    print(f"Tiempo medio: {statistics.mean(tiempos)} segundos")
    print(f"Desviación estándar: {statistics.stdev(tiempos)}")

if __name__ == "__main__":
    medir_lectura()
