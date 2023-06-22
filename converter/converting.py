import pika
from config import settings
from postgre import change_status, get_exts
import io
import ffmpeg 
import subprocess
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
    file_id = body.decode('utf-8')
    print("Received %r" % file_id)
    exts = get_exts(file_id)
    change_status(file_id, 2)
    try:
        cl = S3minio()
        input_data = cl.get_file(file_id=file_id)
        args = (ffmpeg
            .input('pipe:', format=exts[0])
            .output('pipe:', format=exts[1])
            .get_args()
        )
        p = subprocess.Popen(['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output_data = io.BytesIO(p.communicate(input=input_data.read())[0])
        output_data.seek(0)
        cl.upload_file(file=output_data, file_id=file_id)
        print("Upload succesfully")

    except Exception as err:
        print("converting error", err)
    finally:
        # cl.remove_file(file_id=file_id, bucket="upbuck")
        change_status(file_id, 3)


# Подписываемся на очередь и ждем сообщений
channel.basic_consume(queue='hello',
                      on_message_callback=callback,
                      auto_ack=True)

