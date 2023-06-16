from config import settings
import boto3


first_bucket='bucket01'

class s3_minio():

    def __init__(self) -> None:

        self.client = boto3.client('s3',
                    endpoint_url=f'http://{settings.HOST}:{settings.PORT_MINIO}',
                    aws_access_key_id=settings.MINIO_ROOT_USER,
                    aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
                    # config=Config(signature_version='s3v4'),
                    # region_name='us-east-1'
                    )
    s3_resource = boto3.resource('s3',
                endpoint_url=f'http://{settings.HOST}:{settings.PORT_MINIO}',
                aws_access_key_id=settings.MINIO_ROOT_USER,
                aws_secret_access_key=settings.MINIO_ROOT_PASSWORD)


    def create_bucket(self):
        
        # try:
        #     s3.head_bucket(Bucket=bucket_name)
        #     print(f"The bucket {bucket_name} exists")
        # except ClientError:
        #     print(f"The bucket {bucket_name} does not exist")
        try: 
            if not first_bucket in self.client.buckets.all():
                bucket = self.client.create_bucket(Bucket=first_bucket)
        except Exception as exc:
            print("[ERROR]:", exc)
        finally:
            return bucket

    def upload_file(self, file, file_id : str):
        try:
            self.client.upload_fileobj(file, first_bucket, file_id)
        except Exception as exc:
            print("[ERROR]:", exc)
        

    def get_url_to_file(self, file_id : str) -> str:
        try: 
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': first_bucket,
                    'Key': file_id
                },
                )
            return url 
        except Exception as exc:
            print("[ERROR]:", exc)


    def remove_file(self, file_id: str):
        try: 
            self.client.delete_object(Bucket=first_bucket, Key=file_id,)
        except Exception as exc:
            print("[ERROR]:", exc)

