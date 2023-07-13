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

# print(dir(Base.classes)) - DEBUG
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
    sel = [Listings.id, Listings.title, Listings.company, Listings.location, 
            Listings.lat, Listings.lon, Listings.office, Listings.job_type, 
            Listings.salary, Listings.time_recorded, Listings.url]
    listings_records = session.query(*sel).all()
    session.close()
    listings = []
    for listing in listings_records:
        row_data = list(np.ravel(listing))
        listings.append(row_data)
    return listings

if __name__ == '__main__':
    app.run(debug=True)