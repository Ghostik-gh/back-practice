FROM python:3.11.3

WORKDIR /manager

COPY ./requirements.txt /manager/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /manager/requirements.txt

COPY ./app /manager

EXPOSE 8000

# CMD ["python" "./app/main.py"]
# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]