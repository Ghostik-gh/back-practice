from config import settings
import boto3
import botocore

first_bucket='bucket01'
upload_bucket='upbuck'
download_bucket='downbuck'

s3_resource = boto3.resource('s3',
        endpoint_url=f'http://minio:{settings.PORT_MINIO}',
        # endpoint_url=f'http://{settings.HOST}:{settings.PORT_MINIO}',
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD)



def create_bucket(bucket):
    exists = True
    try:
        s3_resource.meta.client.head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False

    if not exists:
        try:
            s3_resource.create_bucket(Bucket=bucket)
        except Exception as err:
            print(err)


def upload_file(file, file_id : str):
    create_bucket(download_bucket)
    try:
        client = s3_resource.meta.client
        client.upload_fileobj(file, download_bucket, file_id)
    except Exception as exc:
        print("[ERROR]:", exc)
    finally:
        client.close()
        print('MINIO CONNECTION CLOSED')  

def get_file(file_id : str):
    client = s3_resource.meta.client
    file = client.get_object(Bucket=upload_bucket, Key=file_id)
    client.close()
    print('MINIO CONNECTION CLOSED')
    return file.get('Body')


def remove_file(file_id: str, bucket:str):
    try: 
        client = s3_resource.meta.client
        client.delete_object(Bucket=bucket, Key=file_id,)
    except Exception as exc:
        print("[ERROR]:", exc)
    finally:
        client.close()
        print('MINIO CONNECTION CLOSED')
