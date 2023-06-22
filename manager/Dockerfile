FROM python:3.11.3

WORKDIR /manager

COPY ./requirements.txt /manager/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /manager/requirements.txt

COPY ./app /manager

EXPOSE 5432
EXPOSE 9000
EXPOSE 8000
EXPOSE 5672

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "80"]