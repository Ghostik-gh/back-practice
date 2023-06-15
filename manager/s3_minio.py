from minio import Minio
from minio.error import S3Error

first_bucket='bucket01'

class s3_minio():

    def __init__(self) -> None:
        self.client = Minio(
        "127.0.0.1:9000",
        access_key="adminadminadmin",
        secret_key="rootrootroot",
        secure=False,
    )

    def create_bucket(self):
        try: 
            if not self.client.bucket_exists(first_bucket):
                self.client.make_bucket(first_bucket)
                print(f"Bucket {first_bucket} created")
            else:
                print(f"Bucket {first_bucket} already exists")
        except S3Error as exc:
            print("error occurred.", exc)

    def upload_file(self, file_id : str, file_path : str):
        try:
            self.create_bucket()
            self.client.fput_object(
                bucket_name=first_bucket, object_name=file_id, file_path=file_path,
            )
        except S3Error as exc:
            print("error occurred.", exc)
        

    def get_url_to_file(self, file_id : str) -> str:
        try: 
            url = self.client.presigned_get_object(
                bucket_name=first_bucket, object_name=file_id
            )
            return url 
        except S3Error as exc:
            print("error occurred.", exc)

    def remove_file(self, file_id: str):
        try: 
            self.client.remove_object(bucket_name=first_bucket, object_name=file_id,)
        except S3Error as exc:
            print("error occurred.", exc)