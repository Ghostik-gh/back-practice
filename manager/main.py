import random
from fastapi import FastAPI, UploadFile

app = FastAPI()

"""
Проверка состояния 
по айди файла ?
"""
@app.get("/check/{filename}")
def check_state(filename: str):
    if 1 == random.randint(0, 1):
        return {'status': "Пока не готово", 'ID': filename}
    return {"Вы можете получить свои данные https://"}

"""
Отправка файла в MinIO
добавление состояния в таблицу
"""
@app.post("/upload/file")
def upload_file(file: UploadFile):
    with open(f'../data/{file.filename}', "wb+") as f:
        f.write(file.file.read())
    return file

"""
Скачивание файла 
через S3 minio ? или раздача через апи 
просто передавать ссылку ? 
"""
@app.get("/download/file")
def download_file(file: UploadFile):
    with open(f'../data/{file.filename}', "wb+") as f:
        f.write(file.file.read())
    return file

"""
uvicorn main:app --reload
useless ?
"""
if __name__=="__main__":
    pass