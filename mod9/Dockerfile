FROM python:3.10.0-slim

RUN mkdir /app

COPY . /app/

WORKDIR /app

RUN python -m pip install -r /app/requirements.txt

ENTRYPOINT ["python", "app.py"]