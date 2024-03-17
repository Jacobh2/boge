from os import getenv
from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sensor.sensors import Sensors
from deps import get_sensors, get_db
from log import setup_logging, setup_uvicorn_logging
from settings import Settings
from contextlib import asynccontextmanager
from scheduler import Scheduler
import logging

settings = Settings()

setup_logging(settings)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler = Scheduler(get_sensors(), get_db())
    scheduler.start()

    yield

    scheduler.stop()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

setup_uvicorn_logging()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/status")
async def get_sensor_status(sensors: Annotated[Sensors, Depends(get_sensors)]):
    return sensors.get_dict()


@app.get("/health")
async def get_health_status(sensors: Annotated[Sensors, Depends(get_sensors)]):
    sensors.check_sensor_status()
    return "OK"


@app.get("/", response_class=HTMLResponse)
async def get_index(
    request: Request, sensors: Annotated[Sensors, Depends(get_sensors)]
):
    logger.info("About to read sensor values")
    data = sensors.get_dict()
    logger.info("Returning data %s", data)
    html = templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "version": getenv("VERSION", "unknown"), **data},
    )
    return html


@app.put("/switch/{on}")
async def switch_sensor_mode(
    on: bool, sensors: Annotated[Sensors, Depends(get_sensors)]
):
    sensors.switch(on)
    return {"ok": True}
