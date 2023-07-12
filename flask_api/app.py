# Import the dependencies.
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
engine = create_engine("sqlite:///../data/listings.db")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Listings = Base.classes.table_listings

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/listings<br/>"
    )

@app.route("/api/v1.0/listings")
def listings():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to retrieve all the stations
    listings_records = session.query(Listings.table_listings).all()

    session.close()

    # # Create a dictionary from the row data and append to a list of precipitation for the year by dates
    # station_list = []
    # for station, name in stations:
    #     station_dict = {}
    #     station_dict["station"] = station
    #     station_dict["name"] = name
    #     station_list.append(station_dict)

    return jsonify(listings_records)

if __name__ == '__main__':
    app.run(debug=True)