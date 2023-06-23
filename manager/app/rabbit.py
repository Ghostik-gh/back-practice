import pika
from config import settings


def que_init():
    credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)

    parameters = pika.ConnectionParameters(host='rabbitmq',
                                        #    host=settings.HOST,
                                        port=settings.PORT_RABBITMQ,
                                        virtual_host='/',
                                        credentials=credentials)

    connection = pika.BlockingConnection(parameters=parameters)
    return  connection.channel()

def send_msg(text : str):
    channel = que_init() 

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=text)

    print(f" [x] Sent {text}")

    channel.close()

