from fastapi import FastAPI, UploadFile
import uvicorn
from s3_minio import s3_minio
import uuid
import postgre 

app = FastAPI()

# TODO FastAPI-users[sqlalchemy] для авторизации

# TODO Pydantic (BaseModel)
# YEP: boto3 вместо minio 
# TODO raise http error
# TODO secret keys
# 

"""
Проверка состояния по uuid файла
"""
@app.get("/check/{file_id}")
def check_state(file_id: str):
    status = postgre.get_status(file_id)
    match status:
        case 0:
            return {'status': 200, 'response': "Файл успешно загружен"}
        case 1:
            return {'status': 200, 'response': "Вы находитесь в очереди"}
        case 2:
            return {'status': 200, 'response': "Идет обработка"}
        case 3:
            return {'status': 200, 'response': f"Вы можете получить свои данные http://127.0.0.1:8000/download/{file_id}"}
        case 4:
            return {'status': 200, 'response': "Файл уже удален"}
        case _:
            return {'status': 500, 'response': "Неверное состояние файла"}

"""
Отправка файла в MinIO
добавление состояния в таблицу
"""
@app.post("/upload/")
def upload_file(file: UploadFile):
    file_id = str(uuid.uuid4())

    try: 
        s3 = s3_minio()
        s3.upload_file(file=file.file, file_id=file_id)
        print("upload")
        # postgre.add_file(file_id, file.filename, file.filename, '.abc')
        return {'status': 200, 'id' : file_id, 'response': f"http://127.0.0.1:8000/download/{file_id}"}
    except Exception as err:
        return{'status': 500, 'error': err}

"""
Скачивание файла 
"""
@app.get("/download/{file_id}")
def download_file(file_id: str):
    # status = postgre.get_status(file_id)
    # if status == 3:
    minio_cl = s3_minio()
    url = minio_cl.get_url_to_file(file_id=file_id)
    # remove_file(file_id=file_id) # удаление файла ?
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
cd manager
uvicorn main:app --reload
"""
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level='debug')