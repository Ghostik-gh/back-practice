from fastapi import FastAPI, UploadFile
import os
from s3_minio import s3_minio
import uuid
import postgre 

app = FastAPI()


# TODO FastAPI-users[sqlalchemy] для авторизации

"""
Проверка состояния по uuid файла
"""
@app.get("/check/{file_id}")
def check_state(file_id: str):
    status = postgre.get_status(file_id)
    match status:
        case 0:
            return {'status': 425, 'response': "Файл успешно загружен"}
        case 1:
            return {'status': 425, 'response': "Вы находитесь в очереди"}
        case 2:
            return {'status': 425, 'response': "Идет обработка"}
        case 3:
            return {'status': 200, 'response': f"Вы можете получить свои данные http://127.0.0.1:8000/download/{file_id}"}
        case 4:
            return {'status': 404, 'response': "Файл уже удален"}
        case _:
            return {'status': 500, 'response': "Неверное состояние файла"}

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
        postgre.add_file(file_id, file.filename, file.filename, '.abc')
        return {'status': 200, 'id' : file_id}
    except Exception as err:
        return{'status': 500, 'error': err}
    finally:
        os.remove(path=abs_path)

"""
Скачивание файла 
"""
@app.get("/download/{file_id}")
def download_file(file_id: str):
    # status = postgre.get_status(file_id)
    # if status == 3:
    minio_cl = s3_minio()
    url = minio_cl.get_url_to_file(file_id=file_id)
    remove_file(file_id=file_id) # удаление файла ?
    return {'status' : 200, "url": url}

"""
Удаление файла из хранилища
"""
@app.get("/remove/{file_id}")
def remove_file(file_id: str):
    try:
        minio_cl = s3_minio()
        url = minio_cl.remove_file(file_id=file_id)
        return {'status' : 200,"url": url}
    except Exception as err:
        return{'status': 500, 'error': err}

"""
uvicorn main:app --reload
useless ?
"""
if __name__=="__main__":
    pass