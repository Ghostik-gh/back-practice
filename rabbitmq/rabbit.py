import sys
import os
sys.path.append(os.getcwd())

import pika
from manager.config import settings

credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)

parameters = pika.ConnectionParameters(host=settings.HOST,
                                       port=settings.PORT_RABBITMQ,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print(" [x] Sent 'Hello World!'")



# Функция, которая будет вызвана каждый раз, когда приходит сообщение
def callback(ch, method, properties, body):
    print("Received %r" % body)


# Подписываемся на очередь и ждем сообщений
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

connection.close()
