import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
measurement = Base.classes.measurement
station = Base.classes.station
session = Session(engine)
year_ago = dt.date(2017, 8, 23) -  dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome! See below for available routes regarding weather data in Honolulu, Hawaii:<br/>"
        f"<br/>"
        f"---------------------------------------------------------<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"  > Displays precipitation in millimetres for the year leading up to the most recent recorded date (2017-08-23).<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"  > Displays a list of all stations.<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>" 
        f"  > Displays temperatures recorded at the most active station (USC00519281) for the year leading up to the most recent recorded date.<br/>"
        f"<br/>"
        f"/api/v1.0/<start><end><br/>"
        f"  > Set a start and end date to determine the minimum, average, and maximum temperatures within the chosen timeframe.<br/>"
        f"  > Enter start and end dates in the following format:<br/> --- If only entering a start date: yyyy-mm-dd <br/> --- If entering both a start and end date: yyyy-mm-dd/yyyy-mm-dd <br/>"
        f"  > If an end date is not given, the date range will be from the chosen start date through to the most recent date.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary
    prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    session.close()
    prcp_dict = dict(prcp)

    # Return the jsonified dictionary
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of all stations
    station_query = session.query(station.station).all()
    session.close()
    station_list = list(np.ravel(station_query)) 

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperatures of the most active station for the previous year of data
    station_activity = session.query(measurement.station, func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
    station_temps = session.query(measurement.date, measurement.tobs).filter(measurement.station == station_activity[0][0]).filter(measurement.date >= year_ago).all()
    session.close()

    temp_list = [] 
    for date, temp in station_temps:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature (C)"] = temp
        temp_list.append(temp_dict)
    
    # Return a JSON list of the temperature observations (TOBS)
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dates(start=None, end=None):
    # Return a JSON list of the min, average, and max temperatures for a specified start or start-end date range
    if not end:
        # When no end date is given - finds min, avg, and max temps for for all dates greater than or equal to the start date 
        min_temp = session.query(func.min(measurement.tobs)).filter(measurement.date >= f"{start}").first()
        avg_temp = session.query(func.avg(measurement.tobs)).filter(measurement.date >= f"{start}").first()
        max_temp = session.query(func.max(measurement.tobs)).filter(measurement.date >= f"{start}").first()
        session.close()
        return jsonify([f"Min Temp: {min_temp[0]} (C), Average Temp: {round(avg_temp[0], 2)} (C), Max Temp: {max_temp[0]} (C)"])
    else:
        # When both a start and end date are given - finds min, avg, and max temps for the date range from the start to the end date
        min_temp = session.query(func.min(measurement.tobs)).filter(measurement.date >= f"{start}").filter(measurement.date <= f"{end}").first()
        avg_temp = session.query(func.avg(measurement.tobs)).filter(measurement.date >= f"{start}").filter(measurement.date <= f"{end}").first()
        max_temp = session.query(func.max(measurement.tobs)).filter(measurement.date >= f"{start}").filter(measurement.date <= f"{end}").first()
        session.close()
        return jsonify([f"Min Temp: {min_temp[0]} (C), Average Temp: {round(avg_temp[0], 2)} (C), Max Temp: {max_temp[0]} (C)"])

if __name__ == '__main__':
     app.run(debug=True)