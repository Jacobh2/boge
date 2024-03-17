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

    logger.info("Starting all sensors...")
    sensors = get_sensors()
    sensors.start_all()

    logger.info("Sensors started, starting scheduler")
    scheduler = Scheduler(sensors, get_db())
    scheduler.start()

    logger.info("Scheduler started, starting app")

    yield

    scheduler.stop()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

setup_uvicorn_logging()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/status")
async def get_sensor_status(sensors: Annotated[Sensors, Depends(get_sensors)]):
    return sensors.get_dict()


def wants_html_response(accept_header: str) -> bool:
    try:
        if not accept_header:
            return False
        accepts = accept_header.split(",")
        if not accepts:
            return False
        return "text/html" in accepts
    except Exception:
        logger.warning("Failed to figure out if we want html response", exc_info=True)


@app.get("/health")
async def get_health_status(
    request: Request, sensors: Annotated[Sensors, Depends(get_sensors)]
):
    # Check if we're coming from an api call
    logger.info("Checking health with %s", request.headers.get("Accept"))
    statuses = sensors.check_sensor_status()

    if wants_html_response(request.headers.get("Accept", "")):
        data = {}
        for name, status in statuses.items():
            data[name] = "Healthy" if status else "Needs Attention"
            data[f"{name}_class"] = "text-success" if status else "text-danger"

        html = templates.TemplateResponse(
            "health.html",
            {"request": request, "version": getenv("VERSION", "unknown"), **data},
        )
        return html

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
