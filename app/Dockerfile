FROM arm64v8/python:3.11 AS build

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

FROM arm64v8/python:3.11-slim

WORKDIR /usr/app/src

COPY --from=build /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

RUN apt-get update && apt-get install -y python3-smbus libgpiod2 && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
