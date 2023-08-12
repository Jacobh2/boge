from typing import Tuple
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import automationhat
from moisture import Moisture
from humidity import Humidity

app = FastAPI()
templates = Jinja2Templates(directory="templates")

moisture = Moisture()
#humidity = Humidity()

def read_relay_voltage() -> float:
    return automationhat.analog.one.read()


def read_water_moisture() -> float:
    global moisture
    value = moisture.read_raw()
    return moisture.get_percentage(value)


# def read_humidity() -> Tuple[float, float]:
#     global humidity
#     h = humidity.try_get_humidity()
#     t = humidity.try_get_temperature()
#     return t, h

@app.get("/test")
async def test():
    return {"ok": True}


def read_all_data(rv, rw):
    # Read data
    relay_on = automationhat.relay.one.is_on()
    switch_status = "checked" if relay_on else ""
    text_status = "On" if relay_on else "Off"
    voltage_value = rv
    temperature, moisture = -1, -1
    percentage = rw
    return {
        "switch_status": switch_status,
        "text_status": text_status,
        "value": voltage_value,
        "temperature": temperature,
        "moisture": moisture,
        "percentage": percentage
    }

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, rw = Depends(read_water_moisture), rv = Depends(read_relay_voltage)):#, rh = Depends(read_humidity)):
    data = read_all_data(rv, rw)
    return templates.TemplateResponse("index.html", {"request": request, **data})


@app.post("/", response_class=RedirectResponse)
async def switch_relay(switch: dict):
    # Here, you can implement the logic to update the switch status
    # For now, we'll just return the received status as a response
    switch_status = switch.get("switch_status", False)
    if switch_status:
        automationhat.relay.one.on()
    else:
        automationhat.relay.one.off()

    return "/"
