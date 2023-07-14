# Import splinter
from splinter import Browser
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

t = time.localtime()
current_time_file = time.strftime("%Y-%m-%d-%H-%M-%S", t)

log = open(f"../logs/scraping_log_{current_time_file}.txt", "a")
log_file = f"../logs/scraping_log_{current_time_file}.txt"

# Create browser object
browser = Browser('chrome')

# Open Indeed
t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

try:
    print(f"Opening Indeed in Chrome...{current_time}", file=log)    
    
    url = "https://www.indeed.com/"
    browser.visit(url)
except:
    print(f"Something went wrong trying to open Indeed in Chrome...{current_time}", file=log)
    print(f"Something went wrong trying to open Indeed in Chrome...{current_time}")
    
    print(f"Logs have been saved to {log_file}", file=log)
    print(f"Logs have been saved to {log_file}")
    
    log.close()
    quit()

# Give the browser time to respond
time.sleep(10)

# Removes the / from the end of the url
url[:-1]

# Array to store results in
data = []

# Function to scrape all the posts on a single page
def scrape_one_page(data, browser):
    # Job Title
    posts_in_page = browser.find_by_css(".jobsearch-ResultsList").find_by_css(".job_seen_beacon")
        
    for post in posts_in_page:
        # Initialize 1D array to store this post's data
        post_data = []
            
        # Grab job id
        try:
            job_id = post.find_by_css("a").first["data-jk"]
            post_data.append(job_id)
        except:
            post_data.append(None)
            
        # Grab job title
        try:
            title = post.find_by_css("span").first.text
            post_data.append(title)
        except:
            post_data.append(None)
            
        # Grab company
        try:
            company = post.find_by_css(".companyName").first.text
            post_data.append(company)
        except:
            post_data.append(None)
            
        # Grab location
        try:
            location = post.find_by_css(".companyLocation").first.text
            post_data.append(location)
        except:
            post_data.append(None)
            
        # Grab job type (if available)
        try:
            job_type = post.find_by_css("[aria-label='Job type']").first.find_by_xpath("..").first.text
            post_data.append(job_type)
        except:
            post_data.append(None)
                
        # Grab salary (if available)
        try:
            salary = post.find_by_css("[aria-label='Salary']").first.find_by_xpath("..").first.text
            post_data.append(salary)
        except:
            try:
                salary = post.find_by_css(".estimated-salary").first.find_by_css("span").first.text
                post_data.append(salary)
            except:
                post_data.append(None)
                
        # Record the time
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
        post_data.append(current_time)
            
        # Grab job url
        try:
            job_url = post.find_by_css("a").first["href"]
            post_data.append(job_url)
        except:
            post_data.append(None)
        
        data.append(post_data)

# Function to scrape all the posts on all pages
def indeed_scraper(data, search_params, browser):
    base_url = url[:-1]
    # Find the what box & search the job title
    what = browser.find_by_id("text-input-what").first
    what.fill(search_params["what"])
    
    # Find the where box & search for the location
    where = browser.find_by_id("text-input-where").first
    where.type(Keys.CONTROL + "a")
    where.type(Keys.BACKSPACE)
    where.fill(search_params["where"])
    
    where.type(Keys.RETURN)
    
    time.sleep(1)
    
    date_posted = browser.find_by_text("Date posted").first
    date_posted.click()
    
    time.sleep(1)
    
    # This can be set to one of these options = ["Last 24 Hours", "Last 3 days", "Last 7 days", "Last 14 days"]
    last_24_hours = browser.find_by_text("Last 24 hours").first
    last_24_hours.click()
    
    last_page = False
    page_count = 0
    
    while not last_page:
        try:  # This code runs for every page except the last page
            next_page_button = browser.find_by_css("[aria-label='Next Page']")
            
            page_count += 1
            print(f"Scraping page {page_count}...", file=log)
            print(f"Scraping page {page_count}...")
        
            post_data = scrape_one_page(data, browser)
                            
            print("Clicking to next page.", file=log)
            print("Clicking to next page.")
            next_page_button.click()
                            
        except:  # This code runs only for the last page
            
            page_count += 1
            print(f"Scraping final page of {page_count} total pages...", file=log)
            print(f"Scraping final page of {page_count} total pages...")
        
            post_data = scrape_one_page(data, browser)
                            
            print("Final page has been scraped.", file=log)
            print("Final page has been scraped.")
            last_page = True
                       
    return data

# Set "what" for the words to search, and "where" for the location search
search_params = {"what": "Data Analyst", "where": "United States"}

# Run the webscraper to collect all listings from all pages for the last 24 hours

t = time.localtime()
current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

print(f"Beginning scraping process...{current_time}", file=log)
print(f"Beginning scraping process...{current_time}")

try:
    indeed_scraper(data, search_params, browser)
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    print(f"Scraping completed successfully! {current_time}", file=log)
    print(f"Scraping completed successfully! {current_time}")
    
    browser.quit()
    print("Browser has been closed.", file=log)
    print("Browser has been closed.")
    
except:
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    print(f"Something went wrong with the scraper.. :(\n{current_time}", file=log)
    print(f"Something went wrong with the scraper.. :(\n{current_time}")
    
    print(f"Logs have been saved to {log_file}", file=log)
    print(f"Logs have been saved to {log_file}")
    
    browser.quit()
    
    print("Browser has been closed.", file=log)
    print("Browser has been closed.")
    log.close()
    quit()

# Name columns for putting the results into a DataFrame
columns = ["id", "title", "company", "location", "job_type", "salary", "time_recorded", "url"]

# Create a Pandas DataFrame
listings_new_df = pd.DataFrame(data, columns = columns)

# Save the updated DataFrame as a .csv file
try:
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)

    file_path = '../data/listings_new.csv'

    listings_new_df.to_csv(file_path, index=False)
    print(f"New results added and saved to file {file_path}\n{current_time}", file=log)
    print(f"New results added and saved to file {file_path}\n{current_time}")
    
except:
    print(f"Something went wrong saving the results to file.", file=log)
    print(f"Something went wrong saving the results to file.")
    
    print(f"Logs have been saved to {log_file}", file=log)
    print(f"Logs have been saved to {log_file}")
    
    log.close()
    quit()

log.close()