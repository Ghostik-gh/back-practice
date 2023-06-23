from config import settings
import boto3
import botocore

first_bucket='bucket01'
upload_bucket='upbuck'
download_bucket='downbuck'

s3_resource = boto3.resource('s3',
        endpoint_url=f'{settings.ENDPOINT_MINIO}',
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



def upload_file( file, file_id : str):
    client = s3_resource.meta.client
    create_bucket(upload_bucket)
    try:
        client.upload_fileobj(file, upload_bucket, file_id)
    except Exception as exc:
        print("[ERROR]:", exc)
    finally:
        client.close()
    

def get_url_to_file( file_id : str, filename : str) -> str:
    try: 
        client = s3_resource.meta.client
        url = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': download_bucket,
                'Key': file_id,
                'ResponseContentDisposition': f'attachment;filename={filename}'
            },
            )
        return url 
    except Exception as exc:
        print("[ERROR]:", exc)
    finally:
        client.close()


def remove_file( file_id: str, bucket:str):
    try: 
        client = s3_resource.meta.client
        client.delete_object(Bucket=bucket, Key=file_id,)
    except Exception as exc:
        print("[ERROR]:", exc)
    finally:
        client.close()

