import numpy as np
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

###################################################
#  Database Setup
###################################################
engine = create_engine("sqlite:///./hawaii.sqlite", echo=False) 

#reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

#Save reference to the tabel
Measurement = Base.classes.measurement
Station = Base.classes.station

###################################################
# Flask setup 
##################################################
app = Flask(__name__)

#################################################
#Flask Routes
################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return jsonify ([
      f"Available Routes:<br/>",
      f"/api/v1.0/precipitation<br/>",
      f"/api/v1.0/stations",
      f"/api/v1.0/tobs",
      f"/api/v1.0/<start>",
      f"/api/v1.0/<start>/<end>",
    ])

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create the session link from Python to db
    session = Session(engine)
    #Query for a year's worth of precipitation 

    #calculate the last date in the table 
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date 1 year ago from the latest date in the database
    yr_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    precip = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date>yr_ago).order_by(Measurement.date.desc()).all()   

    #Put the query results in a dictionary
    precip_dict = dict(precip)
    session.close()
    return jsonify (precip_dict)

if __name__ == "__main__":
    app.run(debug=True)   

@app.route("/api/v1.0/stations")
def stations():
    #Create the session link from Python to db
    session = Session(engine)

    #Query a list of stations return results as json
    station_query = session.query(Measurement.station).all()

    #convert a list of tuples
    station_listing = list(np.ravel(station_query))

    session.close()
    return jsonify (station_listing)

if __name__ == "__main__":
    app.run(debug=True)   


@app.route("/api/v1.0/tobs")
def tobs():   
    #Create the session link from Python to db
    session = Session(engine)
    #Query for a year's worth of temperature observation data

    #calculate the last date in the table 
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date 1 year ago from the latest date in the database
    yr_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
  
    #Query for tobs
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>yr_ago).all()  

    tobs_listing = list(np.ravel(tobs_query))

    session.close()
    return jsonify (tobs_listing)
if __name__ == "__main__":
    app.run(debug=True)   


@app.route("/api/v1/<start>")
def start(start=None):
    #Create the session link from Python to db
    session = Session(engine)
    #return a JSON list of the min, avg and max temp for a given start date
    start_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date>=start).group_by(Measurement.date).all()
    start_list=list(start_query)
    
    session.close()
    return jsonify(start_list)
    
if __name__ == "__main__":
        app.run(debug=True)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    #Create the session link from Python to db
    session = Session(engine)
    #Return a JSON list of the min, avg and max temp for a given start date and end date
    begin_end_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date>=start).filter(Measurement.date<=end).group_by(Measurement.date).all()
    begin_end_dates_list=list(begin_end_dates)


    session.close()
    return jsonify(begin_end_dates_list)

if __name__ == "__main__":
        app.run(debug=True)