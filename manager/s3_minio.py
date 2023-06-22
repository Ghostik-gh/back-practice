from config import settings
import boto3
import botocore

first_bucket='bucket01'
upload_bucket='upbuck'
download_bucket='downbuck'

class S3minio():

    def __init__(self) -> None:

        self.s3_resource = boto3.resource('s3',
                endpoint_url=f'http://{settings.HOST}:{settings.PORT_MINIO}',
                aws_access_key_id=settings.MINIO_ROOT_USER,
                aws_secret_access_key=settings.MINIO_ROOT_PASSWORD)

        self.client = self.s3_resource.meta.client


    def create_bucket(self, bucket):
        exists = True
        try:
            self.s3_resource.meta.client.head_bucket(Bucket=bucket)
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False

        if not exists:
            try:
                self.s3_resource.create_bucket(Bucket=bucket)
            except Exception as err:
                print(err)


    def upload_file(self, file, file_id : str):
        self.create_bucket(upload_bucket)
        try:
            self.client.upload_fileobj(file, upload_bucket, file_id)
        except Exception as exc:
            print("[ERROR]:", exc)
        

    def get_url_to_file(self, file_id : str, filename : str) -> str:
        try: 
            url = self.client.generate_presigned_url(
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


    def remove_file(self, file_id: str, bucket:str):
        try: 
            self.client.delete_object(Bucket=bucket, Key=file_id,)
        except Exception as exc:
            print("[ERROR]:", exc)

