# Dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Reflecting databases
engine = create_engine('sqlite:///../Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect = True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Creating an app
app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return(
        f'Welcome to the Honolulu Weather API created by Soo Bin!</br>'
        f'</br></br>'
        f'Available routes:</br>'
        f'</br>'
        f'/api/v1.0/precipitation</br>'
        f'This page stores precipitation data of Honolulu, HI, from 2010-01-01.</br>'
        f'</br>'
        f'/api/v1.0/stations</br>'
        f'This page lists observation stations located in Honolulu, HI.</br>'
        f'</br>'
        f'/api/v1.0/tobs</br>'
        f'This page stores temperature data of Honolulu, HI, from a year from the last data point.</br>'
        f'</br>'
        f'/api/v1.0/start</br>'
        f'This page shows you the minimum, maximum, and average temperatures for dates</br>'
        f'from the input date to the latest observed date.</br>'
        f'Replace "start" with "yyyy-mm-dd" to start a query.</br>'
        f'</br>'
        f'/api/v1.0/start/end</br>'
        f'This page shows you the minimum, maximum, and average temperatures for dates</br>'
        f'from the input date for start date to the input date for end date.</br>'
        f'Replace "start" and "end" with "yyyy-mm-dd" to start a query.'
    )

# Precipitation data by date
@app.route('/api/v1.0/precipitation')
def prcp():
    prcp_query = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).all()
    prcp_list = []
    
    for prcp in prcp_query:
        prcp_dict = {}
        prcp_dict['date'] = prcp[0]
        prcp_dict['prcp'] = prcp[1]
        prcp_list.append(prcp_dict)

    return(jsonify(prcp_list))

# List of stations
@app.route('/api/v1.0/stations')
def stations():
    stations = session.query(Station.station, Station.name).\
        order_by(Station.station).all()
    stations_list = []
    
    for s in stations:
        s_dict = {}
        s_dict['id'] = s[0]
        s_dict['name'] = s[1]
        stations_list.append(s_dict)

    return(jsonify(stations_list))

# Temperature data within the last 365 days from the last observation date
@app.route('/api/v1.0/tobs')
def tobs():
    last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()

    yy = int(last_date[0][:4])
    mm = int(last_date[0][5:7])
    dd = int(last_date[0][-2:])
    date_diff = dt.date(yy, mm, dd) - dt.timedelta(days = 365)

    temp_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > date_diff).\
        order_by(Measurement.date).all()
    temp_list = []

    for temp in temp_query:
        temp_dict = {}
        temp_dict['date'] = temp[0]
        temp_dict['temp'] = temp[1]
        temp_list.append(temp_dict)

    return(jsonify(temp_list))

# Calculating temperatures for dates between the input date and the latest observed date
@app.route('/api/v1.0/<start>')
def temps(start):
    yy = int(start[:4])
    mm = int(start[5:7])
    dd = int(start[-2:])
    date_diff = dt.date(yy, mm, dd) - dt.timedelta(days = 365)
    
    summary_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).\
        filter(Measurement.date > date_diff).all()
    
    summary = {
        'TMIN': summary_query[0][0],
        'TMAX': summary_query[0][1],
        'TAVG': round(summary_query[0][2], 1)
    }
    
    return(jsonify(summary))

# Calculating temperatures for dates between the input dates
@app.route('/api/v1.0/<start>/<end>')
def temps2(start, end):
    yy1 = int(start[:4])
    mm1 = int(start[5:7])
    dd1 = int(start[-2:])
    start_date = dt.date(yy1, mm1, dd1)

    yy2 = int(end[:4])
    mm2 = int(end[5:7])
    dd2 = int(end[-2:])
    end_date = dt.date(yy2, mm2, dd2)
    
    summary_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date.between(start_date, end_date)).all()
    
    summary = {
        'TMIN': summary_query[0][0],
        'TMAX': summary_query[0][1],
        'TAVG': round(summary_query[0][2], 1)
    }
    
    return(jsonify(summary))

if __name__ == '__main__':
    app.run(debug = True)