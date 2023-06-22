from fastapi import FastAPI, UploadFile
import uvicorn
from s3_minio import S3minio
import uuid
from postgre import add_file, change_status, get_status, get_filename
import rabbit

app = FastAPI()

# TODO FastAPI-users[sqlalchemy] для авторизации

# YEP: Pydantic (BaseModel)
# YEP: boto3 вместо minio 
# TODO raise http error
# YEP: secret keys
# TODO разные конфиги для сервисов
# TODO testing 

"""
Проверка состояния по uuid файла
"""
@app.get("/check/{file_id}")
def check_state(file_id: str):
    try:
        status = get_status(file_id)
        match status:
            case 0:
                return {'status': 200, 'response': "Файл успешно загружен"}
            case 1:
                return {'status': 200, 'response': "Вы находитесь в очереди"}
            case 2:
                return {'status': 200, 'response': "Идет обработка"}
            case 3:
                return {'status': 200, 'response': f"Вы можете получить свои данные", 'url': f"http://127.0.0.1:8000/download/{file_id}"}
            case 4:
                return {'status': 200, 'response': "Такого файла нет или он уже удален"}
            case _:
                return {'status': 500, 'response': "Неверное состояние файла"}
    except Exception as err:
        print("[ERROR]: main.py", err)
        return {'status': 500, 'response': "Неверное состояние файла"}

"""
Отправка файла в MinIO
добавление состояния в таблицу
"""
@app.post("/upload/{end_ext}")
def upload_file(file: UploadFile, end_ext: str):
    file_id = str(uuid.uuid4())
    try: 
        filename=file.filename.split('.')[:-1]
        filename = ''.join(filename)
        add_file(uuid=file_id, filename=filename, start_ext=file.filename.split('.')[-1], end_ext=end_ext)
        s3 = S3minio()
        s3.upload_file(file=file.file, file_id=file_id)
        rabbit.send_msg(text=file_id)
        change_status(uuid=file_id, state=1)
        return {'status': 200, 'id' : file_id, 'response':'Проверить состояние файла', 'url': f"http://127.0.0.1:8000/check/{file_id}"}
    except Exception as err:
        return{'status': 500, 'error': err}

"""
Скачивание файла 
"""
@app.get("/download/{file_id}")
def download_file(file_id: str):
    status = get_status(file_id)
    if status == 3:
        minio_cl = S3minio()
        filename = get_filename(file_id)
        print(filename)
        url = minio_cl.get_url_to_file(file_id=file_id, filename=filename)
        return {'status' : 200, "url": url}
    elif status == 4:
        return {'status': 200, 'response': "Такого файла нет или он уже удален"}
    elif status <= 2:
        return {'status': 200, 'id' : file_id, 'response':'Пока не готово', 'url': f"http://127.0.0.1:8000/check/{file_id}"}
    else:
        return {'status': 500, 'response':'Ошибка сервера, попробуйте заново загрузить'}

"""
Удаление файла из хранилища
как передавать из какого бакета удалять
"""
@app.get("/remove/{file_id}")
def remove_file(file_id: str):
    try:
        minio_cl = S3minio()
        minio_cl.remove_file(file_id=file_id, bucket='upbuck')
        minio_cl.remove_file(file_id=file_id, bucket='downbuck')
        change_status(file_id, 4)
        return {'status' : 200, "response" : "Файл удален"}
    except Exception as err:
        return{'status': 500, 'error': err}

"""
cd manager
uvicorn main:app --reload
"""
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level='debug')