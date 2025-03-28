import pika
import sys

def cancelar_voto(hostname, port, id_voto):
    try:
        credentials = pika.PlainCredentials('alumnomq', 'alumnomq')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=hostname, port=int(port), credentials=credentials)
        )
        channel = connection.channel()
    except Exception as e:
        print(f"Error al conectar al host remoto: {e}")
        exit()

    channel.queue_declare(queue='voto_cancelacion', durable=True)

    mensaje = f"{id_voto}"
    channel.basic_publish(
        exchange='',
        routing_key='voto_cancelacion',
        body=mensaje,
        properties=pika.BasicProperties(delivery_mode=2)  # Mensaje persistente
    )

    print(f" [x] Sent cancelar voto'{mensaje}'")
    connection.close()

def main():
    if len(sys.argv) != 4:
        print("Debe indicar el host, el número de puerto y el ID del voto a cancelar.")
        exit()

    cancelar_voto(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
