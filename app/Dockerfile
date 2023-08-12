FROM arm64v8/python:3.11-slim
# FROM python:3.11

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
