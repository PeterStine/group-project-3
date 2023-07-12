"""
Author: Peter Stine
Date Created: 7/11/2023
Description:
    This script transfers and archives data collected into the "../data" folder in 
    the form of csv files to a single sqlite database file. This is due to eventual
    performance concerns around collecting long-term data in csv files.

    This script is meant to be run as a cron job periodically to back
    up the csv data to a more permanent sqlite database (.db file).  
"""
import pandas as pd
import sqlite3

# Read in data\listings_cleaned.csv in as a pandas dataframe
df_listings = pd.read_csv("data/listings_cleaned.csv")
print(df_listings)

# Open the database file
conn = sqlite3.connect("listings.db")

# Copy the pandas dataframe into the sqlite database
df_listings.to_sql("table_listings", con=conn)
