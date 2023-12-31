from os import getenv

from database import Database
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sensor.sensors import Sensors

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

db = Database(getenv("DB_PATH", "sensors.db"))

sensors = Sensors(db)


@app.get("/status")
async def get_sensor_status():
    return sensors.get_dict()


@app.get("/health")
async def get_health_status():
    sensors.check_sensor_status()
    return "OK"


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    data = sensors.get_dict()
    html = templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "version": getenv("VERSION", "unknown"), **data},
    )
    return html


@app.put("/switch/{on}")
async def switch_sensor_mode(on: bool):
    sensors.switch(on)
    return {"ok": True}


@app.delete("/data")
async def cleanup_data():
    sensors.cleanup_data()
    return {"ok": True}
