#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
import os

ENABLED = 'enabled'
DISABLED = 'disabled'

Icon = "./switch-on.png"
Icoff = "./switch-off.png"
fconfig = "tabmode.conf"

global state
state = ''

if not os.path.isfile(fconfig):
    print("Creating config file")
    with open(fconfig, 'w') as config_file:
        config_file.write(ENABLED)
    state = ENABLED
else:
    with open(fconfig, 'r') as config_file:
        state = config_file.read().strip()
    print(f"keyboard is: {state}")

app = Flask(__name__)

@app.route('/')
def index():
    return 'fliplock api'

@app.route('/toggle')
def toggle():
    global state
    print(state)
    if state == DISABLED:
        print("enable...")
        os.system('evtest --grab /dev/input/event3 &')
        os.system('evtest --grab /dev/input/event9 &')
        with open(fconfig, 'w') as config_file:
            config_file.write(ENABLED)
        state = ENABLED

    elif state == ENABLED:
        print("disable...")
        os.system('pkill evtest')
        with open(fconfig, 'w') as config_file:
            config_file.write(DISABLED)
        state = DISABLED

    return 'success'

app.run(host='localhost', port=4244)
