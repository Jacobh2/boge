FROM arm64v8/python:3.11-slim

RUN pip install fastapi

WORKDIR /usr/app/src

COPY . .
