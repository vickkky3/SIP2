import psycopg2
import time
import statistics
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votoSite.settings")
django.setup()

from votoAppWSClient.models import Voto


# Configuración de conexión a PostgreSQL en VM1
DB_CONFIG = {
    'dbname': 'voto',
    'user': 'alumnodb',
    'password': 'tu_contraseña',
    'host': '127.0.0.1',  # O la IP de VM1
    'port': '15432'
}

#DATABASES={
#    'default': {
#        'NAME': 'voto',
#        'USER': 'alumnodb',
#        'PASSWORD': 'tu_contraseña',
#        'HOST': 'localhost',
#        'PORT': '15432',
#    }
#}
def medir_lectura():
    tiempos = []
    try:
        for _ in range(7):  # Ejecutamos 7 mediciones
            inicio = time.time()
            votos = Voto.objects.all()[:1000]
            fin = time.time()
            tiempos.append(fin - inicio)

    except Exception as e:
        print(f"Error en la conexión: {e}")
        return

    print(f"Tiempo medio: {statistics.mean(tiempos)} segundos")
    print(f"Desviación estándar: {statistics.stdev(tiempos)}")

if __name__ == "__main__":
    medir_lectura()
