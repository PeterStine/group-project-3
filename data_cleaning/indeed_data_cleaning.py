#!/usr/bin/env python
# coding: utf-8

# # indeed_data_cleaning.py
# 
# ---
# 
# ## This will clean the data that was scraped from Indeed.  The location strings will be cleaned into usable locations to feed into Geoapify, coordinates will be determined with Geoapify when possible, and each listing will be tagged as In_person, Hybrid, or Remote.  The results are then saved as both a .csv file and as a .db file for SQLite usage.

# In[ ]:


try:
    # Dependencies and Setup
    import pandas as pd
    import time
    import requests
    import json
    from geoapify_function import single_geocode
    from data_archiver import db_archiver
    import os
    from pathlib import Path

    # Import the API key for Geoapify
    from config import geoapify_key
    
    # Open a file to save logs to
    t = time.localtime()
    current_time_file = time.strftime("%Y-%m-%d-%H-%M-%S", t)

    log = open(f"../logs/cleaning_log_{current_time_file}.txt", "a")
    log_file = f"../logs/cleaning_log_{current_time_file}.txt"
    
    print(f"Log file opened successfully.", file=log)
    print(f"Log file opened successfully.")
    
except:
    # Open a file to save logs to
    t = time.localtime()
    current_time_file = time.strftime("%Y-%m-%d-%H-%M-%S", t)

    log = open(f"../logs/cleaning_log_{current_time_file}.txt", "a")
    log_file = f"../logs/cleaning_log_{current_time_file}.txt"

    print("Something went wrong with importing dependencies, possibly with the Geoapify key or custom geocode function", file=log)
    print("Something went wrong with importing dependencies, possibly with the Geoapify key or custom geocode function")
    
    print(f"Logs have been saved to {log_file}", file=log)
    print(f"Logs have been saved to {log_file}")
    
    log.close()
    quit()


# In[ ]:


# Check if an uncleaned file exists
try:
    # Import uncleaned scraped data
    file_path_new = '../data/listings_new.csv'
    listings_scraped_df = pd.read_csv(file_path_new)

    # Count the total listings
    listings_count = listings_scraped_df['id'].count()
    #print(listings_count)

    # Check that data seems to have loaded correctly
    t = time.localtime()
    current_time_file = time.strftime("%Y-%m-%d-%H-%M-%S", t)
    
    print("New data loaded from file successfully!", file=log)
    print("New data loaded from file successfully!")
    
except:
    print("Something went wrong with loading the uncleaned file", file=log)
    print("Something went wrong with loading the uncleaned file")
    
    print(f"Logs have been saved to {log_file}", file=log)
    print(f"Logs have been saved to {log_file}")
    
    log.close()
    quit()


# In[ ]:


# Create a series of this column for later use
locations = listings_scraped_df['location']


# In[ ]:


# Create a DataFrame which contains only in_person jobs
listings_office_df = listings_scraped_df.loc[~locations.str.startswith('Remote') & ~locations.str.startswith('Hybrid remote')].copy()

# Create a column indicating these are in_person jobs
listings_office_df['office'] = 'in_person'

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

# Get lat, lon for each location
# Create empty lists to hold coordinates

print(f"Beginning Geoapify requests for In_person listings...\n{current_time}", file=log)
print(f"Beginning Geoapify requests for In_person listings...\n{current_time}")

lats_office = []
lons_office = []

for place in listings_office_df['location']:
    try:
        lat, lon = single_geocode(place)
    except:
        lat, lon = None, None
    
    lats_office.append(lat)
    lons_office.append(lon)
    
listings_office_df['lat'] = lats_office
listings_office_df['lon'] = lons_office
        
# Count the results for in_person listings
office_count = listings_office_df['id'].count()

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

print(f"Completed Geoapify requests for {office_count} In_person listings\n{current_time}.", file=log)
print(f"Completed Geoapify requests for {office_count} In_person listings\n{current_time}.")

#listings_office_df.head()


# In[ ]:


# Create a DataFrame which contains only Hybrid Remote jobs
listings_hybrid_df = listings_scraped_df.loc[locations.str.startswith('Hybrid remote')].copy()

# Create a column indicating these are not in_person jobs
listings_hybrid_df['office'] = 'hybrid'

# Remove extra text from location to leave only the city, state (zip)
listings_hybrid_df['location'] = listings_hybrid_df['location'].str.strip('Hybrid remote in ')

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

# Get lat, lon for each location
# Create empty lists to hold coordinates

print(f"Beginning Geoapify requests for Hybrid listings...\n{current_time}", file=log)
print(f"Beginning Geoapify requests for Hybrid listings...\n{current_time}")

lats_hybrid = []
lons_hybrid = []

for place in listings_hybrid_df['location']:
    try:
        lat, lon = single_geocode(place)
    except:
        lat, lon = None, None
    
    lats_hybrid.append(lat)
    lons_hybrid.append(lon)
    
listings_hybrid_df['lat'] = lats_hybrid
listings_hybrid_df['lon'] = lons_hybrid

# Count the results for hybrid listings
hybrid_count = listings_hybrid_df['id'].count()

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

print(f"Completed Geoapify requests for {hybrid_count} Hybrid listings\n{current_time}.", file=log)
print(f"Completed Geoapify requests for {hybrid_count} Hybrid listings\n{current_time}.")

#listings_hybrid_df.head()


# In[ ]:


# Create a DataFrame which contains only Remote jobs
listings_remote_raw_df = listings_scraped_df.loc[locations.str.startswith('Remote')].copy()

# Create a column indicating these are not in_person jobs
listings_remote_raw_df['office'] = 'remote'

# Split this DataFrame into one that has a location for each job and one that does not

# Contains a location
listings_remote_loc_df = listings_remote_raw_df.loc[listings_remote_raw_df['location'].str.startswith('Remote in ')].copy()
# Remove extra text from location to leave only the city, state (zip)
listings_remote_loc_df['location'] = listings_remote_loc_df['location'].str.strip('Remote in ')

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

# Get lat, lon for each location
# Create empty lists to hold coordinates

print(f"Beginning Geoapify requests for Remote listings...\n{current_time}", file=log)
print(f"Beginning Geoapify requests for Remote listings...\n{current_time}")

lats_remote = []
lons_remote = []

for place in listings_remote_loc_df['location']:
    try:
        lat, lon = single_geocode(place)
    except:
        lat,lon = None, None
    
    lats_remote.append(lat)
    lons_remote.append(lon)
    
listings_remote_loc_df['lat'] = lats_remote
listings_remote_loc_df['lon'] = lons_remote

# Does not have a location
listings_remote_only_df = listings_remote_raw_df.loc[~listings_remote_raw_df['location'].str.startswith('Remote in ')].copy()
listings_remote_only_df['lat'] = 42.447317
listings_remote_only_df['lon'] = -71.224500

# Put the two DataFrames back together
listings_remote_df = pd.concat([listings_remote_loc_df, listings_remote_only_df])

# Count the results for remote listings
remote_count = listings_remote_df['id'].count()

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

print(f"Completed Geoapify requests for {remote_count} Remote listings\n{current_time}.", file=log)
print(f"Completed Geoapify requests for {remote_count} Remote listings\n{current_time}.")

#listings_remote_df.head()


# In[ ]:


# Check if any listings were lost or duplicated
if ((office_count + hybrid_count + remote_count) == listings_count):
    print(f"{listings_count} listings were successfully cleaned!", file=log)
    print(f"{listings_count} listings were successfully cleaned!")

elif ((office_count + hybrid_count + remote_count) > listings_count):
    print(f"Some listings may have been duplicated during cleaning.", file=log)
    print(f"Some listings may have been duplicated during cleaning.")
          
elif ((office_count + hybrid_count + remote_count) < listings_count):
    print(f"Some listings may have been lost during cleaning.", file=log)
    print(f"Some listings may have been lost during cleaning.")


# In[ ]:


# Put the three DataFrames back together
listings_temp_df = pd.concat([listings_office_df, listings_hybrid_df])

listings_cleaned_df = pd.concat([listings_temp_df, listings_remote_df])

# Reordering the columns
listings_cleaned_df = listings_cleaned_df[['id', 'title', 'company', 'location', 'lat', 'lon', 'office', 'job_type', 'salary', 'time_recorded', 'url']]

#listings_cleaned_df


# In[ ]:


# Save the updated DataFrame as a .csv file
t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
current_time_file = time.strftime("%Y-%m-%d-%H-%M-%S", t)

# Check if an archived file exists and concatenate to it if so
try:
    file_path_archive = '../data/listings_cleaned.csv'
    
    # Import cleaned archive data
    listings_archive_df = pd.read_csv(file_path_archive)

    # Drops the column that contains the .csv row number
    #listings_archive_df.drop(columns=listings_archive_df.columns[0], axis=1, inplace=True)
    
    # Save the archived file as a backup
    listings_archive_df.to_csv(f"{file_path_archive}_{current_time_file}", index=False)
    
    # Concatenate new data onto the old
    listings_concat_df = pd.concat([listings_archive_df, listings_cleaned_df])
    
    # Overwrite the archive file with the newly updated one
    listings_concat_df.to_csv(file_path_archive, index=False)
    print(f"New cleaned results added to archive and saved to file {file_path_archive}", file=log)
    print(f"New cleaned results added to archive and saved to file {file_path_archive}")
    print(f"The previous data was saved as a backup file {file_path_archive}_{current_time_file}", file=log)
    print(f"The previous data was saved as a backup file {file_path_archive}_{current_time_file}")
    

except:
    try:
        file_path_write = '../data/listings_cleaned.csv'
    
        listings_cleaned_df.to_csv(file_path_write, index=False)
        print(f"New cleaned results saved to file {file_path_write}", file=log)
        print(f"New cleaned results saved to file {file_path_write}")
        
    except:
        print("Something went wrong with saving the results to file", file=log)
        print("Something went wrong with saving the results to file")
    
        print(f"Logs have been saved to {log_file}", file=log)
        print(f"Logs have been saved to {log_file}")
    
        log.close()
        quit()


# In[ ]:


# Save updated file to the SQLite database
t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
db_file = '../data/listings.db'

try:
    # Delete the existing database file so that it can be replaced with the updated one
    if os.path.isfile(db_file):
        os.remove(db_file)
    
    db_archiver()
    
    print(f"New cleaned results saved to database file {db_file}", file=log)
    print(f"New cleaned results saved to database file {db_file}")
    
except:
    print("Something went wrong with saving the results to database file", file=log)
    print("Something went wrong with saving the results to database file")
    
    print(f"Logs have been saved to {log_file}", file=log)
    print(f"Logs have been saved to {log_file}")
    
    log.close()
    quit()


# In[ ]:


log.close()


# In[ ]:




