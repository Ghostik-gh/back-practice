FROM python:3.11.3

WORKDIR /converter

COPY ./requirements.txt /converter/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /converter/requirements.txt

COPY ./app /converter

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# COPY ./ffmpeg.exe /

# CMD ["python" "/converter/main.py"]