FROM python:3.11.3

WORKDIR /converter

COPY ./requirements.txt /converter/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /converter/requirements.txt

COPY ./app /converter

CMD ["python" "./app/main.py"]