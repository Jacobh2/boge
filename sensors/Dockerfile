FROM arm64v8/python:3.11 AS build

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

FROM arm64v8/python:3.11-slim

RUN apt-get update && apt-get install -y libgpiod2 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app/src

COPY --from=build /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["python", "-m", "mqtt.mqtt"]
