from logging import log
import os
import logging
import argparse
import sys
from flask import Flask, request, json
import asyncio
from werkzeug.serving import is_running_from_reloader
from light_state import LightState, StateHelper
from light import Light

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

HOST = '0.0.0.0'

arg_parser = argparse.ArgumentParser(description='Start Woofer server.')
arg_parser.add_argument('-p', '--port',
                        default=80,
                        type=int,
                        help='Port to use for server.',
                        metavar='port',)
PORT = arg_parser.parse_known_args()[0].port

class RequestPaths:
    LIGHT_PATH = '/light'
    SAVE_POWER_PATH = LIGHT_PATH + '/save_power'
    SAVE_BLINK_PATH = LIGHT_PATH + '/save_blink'
    SAVE_FREQUENCY_PATH = LIGHT_PATH + '/save_frequency'
    SAVE_DUTY_CYCLE_PATH = LIGHT_PATH + '/save_duty_cycle'
    SAVE_BRIGHTNESS_PATH = LIGHT_PATH + '/save_brightness'
    SAVE_RED_PATH = LIGHT_PATH + '/save_red'
    SAVE_GREEN_PATH = LIGHT_PATH + '/save_green'
    SAVE_BLUE_PATH = LIGHT_PATH + '/save_blue'

light_state = LightState()
light_ws = Light(light_state)
light_ws.start()

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route(RequestPaths.LIGHT_PATH)
def light():
    return light_state.get_state()

@app.route(RequestPaths.SAVE_POWER_PATH, methods=['POST'])
def savePower():
    power = getObjectFromRequest(request)[StateHelper.POWER_KEY]
    light_state.set_power(power)
    return light_state.get_state()

@app.route(RequestPaths.SAVE_BLINK_PATH, methods=['POST'])
def saveBlink():
    value = getObjectFromRequest(request)[StateHelper.BLINK_KEY]
    light_state.set_blink(value)
    return light_state.get_state()

@app.route(RequestPaths.SAVE_FREQUENCY_PATH, methods=['POST'])
def saveFrequency():
    value = getObjectFromRequest(request)[StateHelper.FREQUENCY_KEY]
    light_state.set_frequency(value)
    light_ws.refresh_period_or_duty_cycle()
    return light_state.get_state()

@app.route(RequestPaths.SAVE_DUTY_CYCLE_PATH, methods=['POST'])
def saveDutyCycle():
    value = getObjectFromRequest(request)[StateHelper.DUTY_CYCLE_KEY]
    light_state.set_duty_cycle(value)
    light_ws.refresh_period_or_duty_cycle()
    return light_state.get_state()

@app.route(RequestPaths.SAVE_BRIGHTNESS_PATH, methods=['POST'])
def saveBrightness():
    value = getObjectFromRequest(request)[StateHelper.BRIGHTNESS_KEY]
    light_state.set_brightness(value)
    return light_state.get_state()

@app.route(RequestPaths.SAVE_RED_PATH, methods=['POST'])
def saveRed():
    value = getObjectFromRequest(request)[StateHelper.RED_KEY]
    light_state.set_red(value)
    return light_state.get_state()

@app.route(RequestPaths.SAVE_GREEN_PATH, methods=['POST'])
def saveGreen():
    value = getObjectFromRequest(request)[StateHelper.GREEN_KEY]
    light_state.set_green(value)
    return light_state.get_state()

@app.route(RequestPaths.SAVE_BLUE_PATH, methods=['POST'])
def saveBlue():
    value = getObjectFromRequest(request)[StateHelper.BLUE_KEY]
    light_state.set_blue(value)
    return light_state.get_state()

def getObjectFromRequest(request):
    return json.loads(request.data.decode())

if __name__ == '__main__':
    app.run(host= HOST, debug=False, port=PORT)