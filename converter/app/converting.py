import os
import pika
from config import settings
from postgre import change_status, get_exts
import io
import ffmpeg 
import subprocess
from s3_minio import get_file, remove_file, upload_file
import logging



credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)

parameters = pika.ConnectionParameters(host=settings.HOST_RABBITMQ,
                                       port=settings.PORT_RABBITMQ,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

# Функция, которая будет вызвана каждый раз, когда приходит сообщение
def callback(ch, method, properties, body):
    file_id = body.decode('utf-8')
    exts = get_exts(file_id)
    print('Received', file_id)
    change_status(file_id, 2)
    try:
        input_data = get_file(file_id=file_id)
        filename=f'{file_id}.{exts[1]}'
        out, err = (ffmpeg
            .input('pipe:0', format=exts[0])
            .output(filename, format=exts[1])
            .run(input=input_data.read(), capture_stdout=True, capture_stderr=True)
        )
        with open(filename, 'rb') as f:
            upload_file(file=f, file_id=file_id)
        os.remove(filename)
        change_status(file_id, 3)
        print("Upload succesfully")
    except ffmpeg.Error as err:
        print("converting error", err)
        change_status(file_id, 4)
    finally:
        remove_file(file_id=file_id, bucket="upbuck")


# Подписываемся на очередь и ждем сообщений
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

