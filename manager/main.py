from fastapi import FastAPI, UploadFile
import os
from s3_minio import s3_minio
import uuid


app = FastAPI()


# TODO FastAPI-users[sqlalchemy] для авторизации

"""
Проверка состояния по uuid файла
"""
@app.get("/check/{file_id}")
def check_state(file_id: str):
    return {'status': 200, 'response': f"Вы можете получить свои данные http://127.0.0.1:8000/download/{file_id}"}
    return {'status': 425, 'response': "Идет обработка"}

"""
Отправка файла в MinIO
добавление состояния в таблицу
"""
@app.post("/upload/file")
def upload_file(file: UploadFile):
    rel_dir_path='../tmp'
    file_id = str(uuid.uuid4())

    if not os.path.exists(rel_dir_path):
        os.makedirs(rel_dir_path)
    
    with open(f'{rel_dir_path}/{file.filename}', "wb+") as f:
        f.write(file.file.read())

    abs_path = os.path.abspath(f'{rel_dir_path}/{file.filename}')

    try: 
        minio_cl = s3_minio()
        minio_cl.upload_file(file_id=file_id, file_path=abs_path)
        return {'status': 200, 'id' : file_id}
    except Exception as err:
        return{'status': 500, 'error': err}
    finally:
        os.remove(path=abs_path)

"""
Скачивание файла 
через S3 minio ? или раздача через апи 
просто передавать ссылку ? 
"""
@app.get("/download/{file_id}")
def download_file(file_id: str):
    minio_cl = s3_minio()
    url = minio_cl.get_url_to_file(file_id=file_id)
    return {'status' : 200,"url": url}

"""
uvicorn main:app --reload
useless ?
"""
if __name__=="__main__":
    pass