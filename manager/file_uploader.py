import random
from minio import Minio
from minio.error import S3Error


class s3_minio():

    # def __init__(self) -> None:
    #     client = Minio(
    #     "127.0.0.1:9000",
    #     access_key="adminadminadmin",
    #     secret_key="rootrootroot",
    #     secure=False
    # )

    client = Minio(
        "127.0.0.1:9000",
        access_key="adminadminadmin",
        secret_key="rootrootroot",
        secure=False
    )

    def create_bucket(self):
        if self.client.bucket_exists("bucket01"):
            print("Bucket 'bucket01' already exists")
        else:
            self.client.make_bucket("bucket01")
            print("Bucket 'bucket01' created")

    def upload_file(self, file_id : str):
        self.create_bucket()
        self.client.fput_object(
            bucket_name="bucket01", object_name=file_id, file_path="C:\\Users\\Фёдор\\OneDrive\\Документы\\MTUCI\\back-practice\\docker-compose.yml", 
        )

    def get_url_to_file(self, file_id : str):
        self.create_bucket()
        url = self.client.presigned_get_object(
            bucket_name="bucket01", object_name=file_id
        )
        print(url)
        return url


try:
    file_id = str(random.randint(0, 1000))+'.txt'
    s3_minio().upload_file(file_id=file_id)
    s3_minio().get_url_to_file(file_id=file_id)
except S3Error as exc:
    print("error occurred.", exc)


# def main():
#     # Create a client with the MinIO server playground, its access key
#     # and secret key.
#     client = Minio(
#         "127.0.0.1:9000",
#         access_key="adminadminadmin",
#         secret_key="rootrootroot",
#         secure=False
#     )


#     # Make 'bucket01' bucket if not exist.
#     # client.make_bucket("bucket01")
#     found = client.bucket_exists("bucket01")
#     if not found:
#         client.make_bucket("bucket01")
#         print("Bucket 'bucket01' created")
#     else:
#         print("Bucket 'bucket01' already exists")

#     file_id = str(random.randint(0, 1000))+'.txt'

#     client.fput_object(
#         bucket_name="bucket01", object_name=file_id, file_path="C:\\Users\\Фёдор\\OneDrive\\Документы\\MTUCI\\back-practice\\docker-compose.yml", 
#     )

#     result = client.stat_object(
#         bucket_name="bucket01", object_name=file_id
#     )

#     print(
#     "last-modified: {0}, size: {1}".format(
#         result.last_modified, result.size,
#     ),)

#     url = client.presigned_get_object(
#         bucket_name="bucket01", object_name=file_id
#     )

#     print(url)


# import boto3

# # установка параметров подключения к MinIO
# s3 = boto3.client(
#     's3',
#     endpoint_url='http://localhost:9000',
#     aws_access_key_id='minio',
#     aws_secret_access_key='minio123'
# )

# # загрузка файла в бакет
# filename = 'file.txt'
# bucket_name = 'bucket01'
# with open(filename, 'rb') as f:
#     s3.upload_fileobj(f, bucket_name, filename)