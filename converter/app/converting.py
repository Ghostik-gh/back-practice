import pika
from config import settings
from postgre import change_status, get_exts
import io
import ffmpeg 
import subprocess
from s3_minio import get_file, remove_file, upload_file



credentials = pika.PlainCredentials(settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS)

parameters = pika.ConnectionParameters(host='rabbitmq',
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
    print('========================\nclient')
    exts = get_exts(file_id)
    print(exts)
    change_status(file_id, 2)
    print('change status')
    try:
        print('========================')
        print('client')
        print('client S3 CREATED')
        input_data = get_file(file_id=file_id)
        print('get FILE')
        args = (ffmpeg
            .input('pipe:', format=exts[0])
            .output('pipe:', format=exts[1])
            .get_args()
        )
        p = subprocess.Popen(['ffmpeg'] + args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        output_data = io.BytesIO(p.communicate(input=input_data.read())[0])
        output_data.seek(0)
        upload_file(file=output_data, file_id=file_id)
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

