import os
import logging
import argparse
import sys
from flask import Flask, request, json
import asyncio
from werkzeug.serving import is_running_from_reloader
from light_state import LightState, StateHelper

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

lightState = LightState()
initialState = lightState.getState()

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route(RequestPaths.LIGHT_PATH)
def light():
    return lightState.getState()

@app.route(RequestPaths.SAVE_POWER_PATH, methods=['POST'])
def savePower():
    power = getObjectFromRequest(request)[StateHelper.POWER_KEY]
    lightState.setPower(power)
    # Audio.setPower(power)
    return lightState.getState()

def getObjectFromRequest(request):
    return json.loads(request.data.decode())

if __name__ == '__main__':
    app.run(host= HOST, debug=True, port=PORT)