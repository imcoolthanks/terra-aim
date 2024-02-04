# py -m flask --app="prototype/app.py" run

import sqlite3 as sql
from flask import Flask, request, jsonify
from flask import render_template
from database import create_examples_gyroscope, create_examples_position, insert_gyroscope_database, insert_position_database, list_gyroscope, list_position, create_examples_heartrate, insert_heartrate_database, list_heartrate, create_examples_clicked, insert_clicked_database, list_clicked
from coordinateMap import CoordinateMap

import requests
from datetime import datetime, timedelta

import os

app = Flask(__name__)

#Basic functions to load each page, need modifications
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/upload_gyroscope/", methods = ['POST', 'GET'])
def upload_gyroscope():            
    if request.method == 'POST':
        # Get gyroscope data
        res = request.json
        yaw = res['BAM']
        pitch = res['POW']

        # Pre-process data

        currentTime = datetime.now()

        insert_gyroscope_database(currentTime, yaw, pitch)   
        return render_template('success.html')
    return render_template('fail.html')

@app.route("/upload_heartrate/", methods = ['POST', 'GET'])
def upload_heartrate():                
    if request.method == 'POST':
        # Get heartrate data
        res = request.json['d']
        ts = res['ts']
        heartrate = res['val']
        insert_heartrate_database(ts, heartrate)
        return render_template('success.html')
    return render_template('fail.html')

@app.route("/upload_position/", methods = ['POST', 'GET'])
def upload_position():                
    if request.method == 'POST':
        res = request.json
        dx = res['x']
        dy = res['y']

        currentTime = datetime.now()

        insert_position_database(currentTime, dx, dy)   
        return render_template('success.html')
    return render_template('fail.html')

@app.route("/get_average_heartrate/", methods = ['POST', 'GET'])
def get_average_heartrate():
    if request.method == 'GET':
        heartrates = list_heartrate()
        avg = sum(map(lambda x: x[1], heartrates)) / len(heartrates)
        data = {
            "value" : avg
        }
        return jsonify(data)
    return render_template('fail.html')

@app.route("/get_position/", methods = ['POST', 'GET'])
def calculate_pos():                
    if request.method == 'GET':
        currentTime = datetime.now()

        conn = sql.connect("data.db")
        cur = conn.cursor()

        # Get gyroscope data
        query = """SELECT *
                FROM gyroscope
                WHERE gyroscope.time < ?
                ORDER BY gyroscope.time DESC
                LIMIT 1
                """
        cur.execute(query, (currentTime,))
        rows = list(cur.fetchall())

        yaw = rows[0][1]
        pitch = rows[0][2]

        # Get position data
        query = """SELECT *
        FROM position
        WHERE position.time < ?
        ORDER BY position.time DESC
        LIMIT 1
        """

        coordinateMap = CoordinateMap(95, 50, 28.12, 25.5, 14.3)
        cur.execute(query, (currentTime,))
        rows = list(cur.fetchall())
        
        dx = rows[0][1]
        dy = rows[0][2]
        
        # Call heyang's function
        x, y = coordinateMap.get_position(-dx, -dy, yaw, pitch)

        print(x, y)

        # TODO: send x and y to the frontend
        data = { 
            "projectedX" : 0.5, 
            "projectedY" : 0.5, 
        }
        return jsonify(data)
    return render_template('fail.html')

@app.route("/upload_time_fired/", methods = ['POST', 'GET'])
def upload_time_fired():
    if request.method == 'POST':
        time_fired = request.json['time_fired']
        insert_clicked_database(time_fired)        
        return render_template('success.html')
    return render_template('fail.html')

@app.route("/check_fired/", methods = ['POST', 'GET'])
def check_fired():
    print("In check_fired")
    if request.method == 'GET':
        print("GETTTTTT")
        currTime = datetime.now()
        deltaCurrTime = datetime.now() - timedelta(seconds=0.3)

        conn = sql.connect("data.db")
        cur = conn.cursor()
        query = """SELECT *
                FROM clicked
                WHERE clicked.time > ? 
                ORDER BY clicked.time DESC
                LIMIT 1
                """
        cur.execute(query, (deltaCurrTime, ))
        fireRows = list(cur.fetchall())
        x = 0
        y = 0
        
        if len(fireRows) > 0:
            # Delete all entries
            query = """DELETE FROM clicked"""
            cur.execute(query)

            currentTime = datetime.now()

            # Get gyroscope data
            query = """SELECT *
                    FROM gyroscope
                    WHERE gyroscope.time < ?
                    ORDER BY gyroscope.time DESC
                    LIMIT 1
                    """
            cur.execute(query, (currentTime,))
            rows = list(cur.fetchall())

            yaw = rows[0][1]
            pitch = rows[0][2]

            # Get position data
            query = """SELECT *
                    FROM position
                    WHERE position.time < ?
                    ORDER BY position.time DESC
                    LIMIT 1
                    """

            coordinateMap = CoordinateMap(95, 50, 28.12, 25.5, 14.3)
            cur.execute(query, (currentTime,))
            rows = list(cur.fetchall())
            
            dx = rows[0][1]
            dy = rows[0][2]

            dx = 100 - dx
            dy = 56.25 - dy
            
            # Call heyang's function
            x, y = coordinateMap.get_position(dx, dy, yaw, pitch)
            print(x, y)
        
        data = {
            "fired" : True,
            "projectedX" : x,
            "projectedY" : y
        }

        return jsonify(data)
    print("Did not go into get func in check_fired")    
    return render_template('fail.html')

