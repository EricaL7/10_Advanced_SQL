# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)
base.classes.keys()

# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

#Sample
@app.route("/")
def home():
    return (f"Available Routes:<br/>"
           f"/api/v1.0/precipitation<br/>" 
           f"/api/v1.0/tobs<br/>"
           f"/api/v1.0/startdate<br/>"
           f" /api/v1.0/startdate/enddate<br/>"
           f"Start/end date must be YYYY-MM-DD")


@app.route("/api/v1.0/precipitation")
def precipitation(): 
   year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   data_precip = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
   precip_dict = {measurement.date:measurement.prcp for measurement.date, measurement.prcp in data_precip}
   return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    total_stations = session.query(station.station).all()
    transition = np.ravel(total_stations)
    station_list =[transition]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def active_stations():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    most_active_12 = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= year_ago).all()
    transition = np.ravel(most_active_12)
    active_station_list =[transition]
    return jsonify(active_station_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end="2017-08-23"):
   calculation = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <=end).all()
   date_stats= {}
   date_stats["TMIN"]= calculation[0][0]  
   date_stats["TAVG"]= round(calculation[0][1], 2)
   date_stats["TMAX"]= calculation[0][2]  
   return date_stats
   
if __name__ == '__main__':
    app.run(debug=True)

   



