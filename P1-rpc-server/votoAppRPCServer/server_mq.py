import os
import sys
import django
import pika

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votoSite.settings')
django.setup()

from votoAppRPCServer.models import Censo, Voto

def main():
    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()

    hostname = sys.argv[1]
    port = sys.argv[2]

    # Configurar credenciales
    credentials = pika.PlainCredentials('alumnomq', 'alumnomq')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=hostname, port=int(port), credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='voto_cancelacion', durable=True)

    def callback(ch, method, properties, body):
        try:
            # Decodificar el mensaje recibido (que debería ser el ID del voto)
            voto_id = body.decode()
            print(f" [x] Se ha recibido el voto {voto_id}")

            # Buscar el voto en la base de datos
            voto = Voto.objects.filter(id=voto_id).first()

            if voto:
                # Modificar el código de respuesta del voto a '111' (cancelado)
                voto.codigoRespuesta = '111'
                voto.save()

                print(f" [x] El voto {voto_id} se ha cancelado correctamente.")
            else:
                print(f" [x] El voto {voto_id} no se ha encontrado.")
            
        except Exception as e:
            print(f" [x] Error al procesar el voto: {e}")

    channel.basic_consume(queue='voto_cancelacion', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)