import numpy as np
from math import sqrt
import math
from flask import Flask,render_template,request,make_response
import requests
import json
import socket
import threading

import asyncio
import websockets

app = Flask(__name__)

yValues = [60] * 50


@app.route("/getHeartRate", methods=["POST"])
def getHeartRate():
    data = request.get_json()
    global yValues
    newRate = data
    yValues = yValues[1:len(yValues)]
    yValues.append(newRate)
    return ("nothing")

@app.route("/requestUpdate", methods=["POST"])
def requestUpdate():
    global yValues
    return yValues



def handle(res):
    opcode = res ['op']
    if opcode == 5:
        # newRate = res["d"]["val"]
        print(res)

        requests.post("http://165.227.237.10/upload_heartrate/", json=res)
        print("this is running")

def getAuth():
    dev_id = "antiterrarism-testing-LCwQDA4DAz"
    api_key = "-YVACpXpAiLd-HZ5UcH7wrb5whGxD4ZX"

    headers = {
        "dev-id": dev_id,
        "x-api-key": api_key
    }

    response = requests.post("https://ws.tryterra.co/auth/developer", headers=headers)

    response = json.loads(response.text)

    print(response)

    return response ["token"]

async def hello():
    uri = "wss://ws.tryterra.co/connect"
    token = getAuth()
    print(token)
    auth = {
        "op": 3,
        "d": {
            "token": token,
            "type": 1
        }
    }


    async with websockets.connect(uri) as websocket:

        hello = json.loads(await websocket.recv())

        heartbeat = hello ["d"]["heartbeat_interval"]

        await websocket.send(json.dumps(auth))

        while True:
            await websocket.send(json.dumps({"op": 0}))
            res = json.loads(await websocket.recv())

            handle(res)

            res = json.loads(await websocket.recv())
            handle(res)

def foo():
    asyncio.get_event_loop().run_until_complete(hello())

def bar():
    app.run(host="localhost", port = 8000)


foo()