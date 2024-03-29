FROM arm64v8/python:3.11 AS build

WORKDIR /usr/app/src

COPY requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

FROM arm64v8/python:3.11-slim

WORKDIR /usr/app/src

COPY --from=build /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["python", "-m", "mqtt.mqtt"]
