# group-project-3
PURPOSE:  Develop a map of Indeed.com job listings for "Data Scientist" in the United States.

METHODS:  Indeed.com job listings were scraped using a Python script with Splinter and Selenium packages, with a keyword search for "Data Scientist," the location set to "United States," and the Date Posted option set for "The Last 14 days."  Another Python script utilizing Pandas was used to clean this data, cleaning up the location strings to provide usable search strings that could be entered into Geoapify to get coordinates for mapping.  The jobs were also sorted into In Person, Hybrid, and Remote.  Link url's to the detailed job listing on Indeed.com were provided for each listing.  The data was stored both as a .csv file and as a .db file.  The map was created from JavaScript and HTML, which pulled the data from a url on GitHub where the .csv file was stored.  A Flask API was also created for the data, but was not used for the mapping in this stage of development.

DIRECTORIES and FILES:

The main directory contains the .gitignore and README.md (which is this document).

/data
This directory contains the raw scraped data (listings_new.csv), and the cleaned data from that file in two forms (listings_cleaned.csv and listings.db).  When new data is scraped, the listings_new.csv file is overwritten.  The listings_cleaned.csv and listings.db files have the new data appended to them, and the previous version of the listings_cleaned.csv file which is being updated is saved as a backup file with the date, in case something goes wrong while appending new data.

/data_cleaning
This directory contains 5 files.  The file data_archiver.py is a Python function that loads the existing listings_cleaned.csv file, drops any duplicate data based on the unique job id scraped from Indeed.com, and saves the data as the listings.db file.  The file geoapify_function.py is a Python function that takes in a string as an argument and performs a Geoapify API request using that string as the location to return latitude and longitude.  The file indeed_data_cleaning.ipynb is a Jupyter Notebook file which was used to develop the indeed_data_cleaning.py script.  The file indeed_data_cleaning.py uses the data_archiver and geoapify_function scripts; it loads the raw scraped data from data/listings_new.csv, cleans the location string to remove extra text from the website to ideally leave only location information like city, state, zip code, performs Geoapify requests to get coordinates for each location, and saves the data as /data/listings_cleaned.csv for use in the mapping.  The file simple_db_ready.ipynb was used to debug the cleaning and database storage scripts.

/flask_api
This directory contains a single file, app.py, which creates a Flask API serving the listings.db data, which in future development might be used to serve data to the mapping JavaScript.

/logs
The scripts indeed_webscraper.py and indeed_data_cleaning.py save various statements during processing that indicate its activity, and could be looked at for debugging.  These would be especially useful if future development led to these scripts being run on an automated schedule.

/mapping
This directory contains the mapping JavaScript code in /static/js/logic.js, /static/css/style.css, and the HTML code in index.html which creates the map.  The map itself has a selector to show all individual listings, In Person listings only, Hybrid listings only, Remote listings only, or all listings in a cluster map.  Many of the Remote listings include a location (likely the location of the employer) and are included on the map at those locations.


