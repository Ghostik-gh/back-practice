from minio import Minio
from minio.error import S3Error


def main():
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "127.0.0.1:9000",
        access_key="adminadminadmin",
        secret_key="rootrootroot",
        secure=False
    )


    # Make 'my-bucket' bucket if not exist.
    client.make_bucket("my-bucket")
    # found = client.bucket_exists("my-bucket")
    # if not found:
    #     client.make_bucket("my-bucket")
    # else:
    #     print("Bucket 'my-bucket' already exists")
    print("Bucket 'my-bucket' created")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        bucket_name="my-bucket", object_name= "test.txt", file_path="C:\\Users\\Фёдор\\OneDrive\\Документы\\MTUCI\\back-practice\\Readme.md",
    )


# if __name__ == "__main__":
try:
    main()
except S3Error as exc:
    print("error occurred.", exc)

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
# bucket_name = 'my-bucket'
# with open(filename, 'rb') as f:
#     s3.upload_fileobj(f, bucket_name, filename)