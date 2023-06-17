import pika
from config import settings
from postgre import change_status
import time
from ffmpeg import FFmpeg, Progress
from s3_minio import S3minio



credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)

parameters = pika.ConnectionParameters(host=settings.HOST,
                                       port=settings.PORT_RABBITMQ,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

# Функция, которая будет вызвана каждый раз, когда приходит сообщение
def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    print(body)
    print("Received %r" % body)
    change_status(body, 2)

    file = S3minio().get_file(body).get('Body')    
    print(file)
    print("========================================")

    # def main():
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input("long.mp4")
        .output(
            "out",
            {"codec:a": "pcm_s16le"},
            vn=None,
            f="wav",
        )
    )

    @ffmpeg.on("progress")
    def on_progress(progress: Progress):
        print(progress)

    print("========================================")
    ffmpeg.execute()
    # wave_bytes = ffmpeg.execute()
    # print(wave_bytes)


    time.sleep(10)
    change_status(body, 3)


# Подписываемся на очередь и ждем сообщений
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

