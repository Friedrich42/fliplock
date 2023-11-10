#!/usr/bin/env python
# encoding: utf-8
import atexit
import os
from pathlib import Path
from typing import Union

from flask import Flask
from loguru import logger

DEVICES_TO_GRAB = ["/dev/input/event3", "/dev/input/event9"]

# Create log folder
Path("./logs").mkdir(exist_ok=True)


# Set up the logger
logger.remove()
logger.add("./logs/latest.log", rotation="10 MB", retention="3 days", compression="zip", enqueue=True, serialize=True, level="DEBUG")

ENABLED = 'enabled'
DISABLED = 'disabled'

fconfig = "tabmode.conf"

global state
# disabled by default
state = DISABLED

@logger.catch()
def get_state() -> Union[ENABLED, DISABLED]:
    global state

    if not os.path.isfile(fconfig):
        logger.debug("Creating config file")
        with open(fconfig, 'w') as config_file:
            config_file.write(state)
        return state
    else:
        with open(fconfig, 'r') as config_file:
            state = config_file.read().strip()
        return state

@logger.catch()
def save_state(state: Union[ENABLED, DISABLED]):
    with open(fconfig, 'w') as config_file:
        config_file.write(state)

@logger.catch()
def block_devices():
    for dev in DEVICES_TO_GRAB:
        os.system(f'evtest --grab {dev} &')

@logger.catch()
def unblock_devices():
    os.system('pkill evtest')

@logger.catch()
def toggle_state(current_state: Union[ENABLED, DISABLED]) -> Union[ENABLED, DISABLED]:
    global state
    if current_state == DISABLED:
        logger.debug("enable...")
        block_devices()
        state = ENABLED
    elif current_state == ENABLED:
        logger.debug("disable...")
        unblock_devices()
        state = DISABLED

    save_state(state)
    return state

atexit.register(lambda: toggle_state(DISABLED))

app = Flask(__name__)

@app.route('/')
@logger.catch()
def index():
    return 'fliplock api'

@app.route('/toggle')
@logger.catch()
def toggle():
    global state

    # flip state
    logger.info(f"state is {state}. flipping...")
    state = toggle_state(ENABLED if state == DISABLED else DISABLED)
    logger.info(f"flipped state to {state}")

    return f"Tablet mode is {state}"

if __name__ == "__main__":
    app.run(host='localhost', port=4244)
